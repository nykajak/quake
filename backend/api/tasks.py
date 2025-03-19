from collections import defaultdict
from flask_mail import Message
from api import db,mail
from api.models import *
# from api.workers import celery
from datetime import datetime, timedelta

# @celery.task()
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

    for user in User.query.filter():
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
            # break

# sendEmail()