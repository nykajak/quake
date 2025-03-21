from collections import defaultdict
from flask_mail import Message
from flask import render_template_string
from api import db,mail
from api.models import *
from api.workers import celery
from datetime import datetime, timedelta
from celery.schedules import crontab

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        30,
        add.s(3,2)
    )

@celery.task()
def add(a,b):
    return a + b

@celery.task()
def sendEmail():
    # today = datetime.now()
    # tomorrow = today + timedelta(days = 1)

    today = datetime(day=1,month=1,year=2025)
    tomorrow = datetime(day=1,month=2,year=2025)

    query = db.session.query(Quiz,Chapter,Subject).join(Chapter, Chapter.id == Quiz.chapter_id).join(Subject, Subject.id == Chapter.subject_id)
    query = query.filter(Quiz.dated < tomorrow, Quiz.dated > today)
    
    pending_subjects = defaultdict(set)
    pending_quizes = defaultdict(set)
    for quiz,chapter,subject in query:
        pending_subjects[subject].add(chapter.name)
        pending_quizes[chapter].add(quiz)

    for user in User.query.filter(User.is_admin == 0):
        notify_for = set(user.subjects).intersection(set(pending_subjects.keys()))
        if len(notify_for):
            msg = [f"{user.name}, you have pending quizes for the following today!"]
            for subject in notify_for:
                msg.append(f"Subject: {subject.name}")
                chapter_names = pending_subjects[subject]
                for chapter_name in chapter_names:
                    msg.append(f"Chapter: {chapter_name}")
                    for quiz in pending_quizes[chapter]:
                        msg.append(f"Quiz {quiz.id}")
            
            msg_str = "\n".join(msg)
            msg = Message("Daily reminder from Quake",sender="jakyn@gmail.com",recipients=[user.email])
            msg.body = msg_str
            mail.send(msg)

@celery.task()
def make_summary():
    """
       For each user, create a report of summary of quiz attempts within last month
    """

    # Bounding dates (currently hardcoded!)
    start_of_month = datetime(day=1,month=1,year=2025)
    end_of_month = datetime(day=1,month=2,year=2025)

    # Find all quizes in current month and map it to subject
    quizes = Quiz.query.filter(Quiz.dated < end_of_month, Quiz.dated > start_of_month)
    mapping = defaultdict(set)
    for quiz in quizes:
        mapping[quiz.chapter.subject].add(quiz)

    # Iterate over each user and detect attempted quizes
    for user in User.query.filter(User.is_admin == 0):
        quiz_set = set()
        for subject in user.subjects:
            quiz_set = quiz_set.union(mapping[subject])

        msg = []
        msg.append(f"Hi {user.name}, here's your monthly report!")
        msg.append(f"You had {len(quiz_set)} quizes due this month. Let's see how you did!")
        
        if quiz_set:
            accuracy = 0
            num_questions = 0
            for quiz in quiz_set:

                query = db.session.query(Response, Question).join(Question, Question.id == Response.question_id)
                query = query.filter(Response.quiz_id == quiz.id)
                question_count = query.count()
                query = query.filter(Response.user_id == user.id)
                response_count = query.count()
                query = query.filter(Response.marked == Question.correct)
                correct_count = query.count()

                msg.append("")
                msg.append(f"Quiz #{quiz.id}")
                msg.append(f"No of questions in quiz: {question_count}")
                msg.append(f"No of questions attempted: {response_count}")
                msg.append(f"No of correct answers: {correct_count}")
                
                if question_count > 0:
                    accuracy += correct_count
                    num_questions += question_count

            accuracy = accuracy / num_questions
            msg.append("")
            msg.append(f"Your accuracy this month was: {accuracy * 100:.2f}%!")

        msg_str = "\n".join(msg)
        msg = Message("Daily reminder from Quake",sender="jakyn@gmail.com",recipients=[user.email])
        msg.body = msg_str
        mail.send(msg)
