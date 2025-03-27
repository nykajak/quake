from collections import defaultdict
from flask_mail import Message
from flask import render_template
from api import db,mail
from api.models import *
from api.workers import celery
from datetime import datetime, timedelta
from calendar import monthrange
from celery.schedules import crontab
import os

from api.blueprints.admin.scores import recompute_score_one

@celery.task()
def scheduledDailyReminder():
    """
        Scheduled task #1 - Send daily email to remind of upcoming all users of
        upcoming quizes for the day. Requires bulk sending of emails.

        Trigger: Daily at 00:01 am
    """

    # Computing bounds of quiz times (should be for the upcoming day only!)
    today = datetime.now()
    tomorrow = today + timedelta(days = 1)

    # Fetching all relevant quizes
    query = db.session.query(Quiz,Chapter,Subject).join(Chapter, Chapter.id == Quiz.chapter_id).join(Subject, Subject.id == Chapter.subject_id)
    query = query.filter(Quiz.dated < tomorrow, Quiz.dated > today)
    
    # Populating mapping to construct subject - chapter - quiz heirarchy
    pending_subjects = defaultdict(set)
    pending_quizes = defaultdict(set)
    for quiz,chapter,subject in query:
        pending_subjects[subject].add(chapter.name)
        pending_quizes[chapter].add(quiz)

    # Using default upper limit of infinity for MAIL_MAX_EMAILS
    # Therefore connection will stay open until all emails sent
    # Best practice to be followed when bulk emailing.
    with mail.connect() as conn:
        for user in User.query.filter(User.is_admin == 0):
            # Finding overlap between subjects user enrolled for and subjects with quizes due today
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
                
                # Construction and sending of email
                msg_str = "\n".join(msg)
                msg = Message("Daily reminder from Quake",sender="jakyn@gmail.com",recipients=[user.email])
                msg.body = msg_str
                conn.send(msg)

@celery.task()
def scheduledMonthlyReport():
    """
        Scheduled task #2 - Create a summary of all quiz attempts in the last month per user
        in a html/pdf format and send it via email. Requires bulk sending of emails.

        Trigger: Monthly at 1st of the month
    """

    # Bounding dates for the month!
    start_of_month = datetime.now()
    days_in_month = monthrange(month=start_of_month.month,year=start_of_month.year)[1]
    end_of_month = start_of_month + timedelta(days = days_in_month)

    # Find all quizes in current month and map it to subject
    quizes = db.session.query(Quiz,Subject)
    quizes = quizes.join(Quiz.chapter).join(Chapter.subject)
    quizes = quizes.filter(Quiz.dated < end_of_month, Quiz.dated > start_of_month)

    mapping = defaultdict(set)
    for quiz,subject in quizes:
        mapping[subject].add(quiz)

    # For bulk emailing
    with mail.connect() as conn:
        # Iterate over each user and detect attempted quizes
        for user in User.query.filter(User.is_admin == 0):
            quiz_set = set()
            for subject in user.subjects:
                quiz_set = quiz_set.union(mapping[subject])

            quizes = []
            if quiz_set:
                accuracy = 0
                num_questions = 0
                for quiz in quiz_set:
                    score = Score.query.filter(Score.user_id == user.id, Score.quiz_id == quiz.id).scalar()
                    if score is None:                    
                        question_count = quiz.questions.count()
                        attempted_count, correct_count = recompute_score_one(quiz.id,user.id)
                        score = Score(user_id = user.id, quiz_id = quiz.id, attempted_count = attempted_count, question_count = question_count, correct_count = correct_count)
                        db.session.add(score)
                        db.session.commit()

                    else:
                        attempted_count = score.attempted_count
                        correct_count = score.correct_count
                        question_count = score.question_count

                    quizes.append({
                        "id": quiz.id,
                        "question_count": question_count,
                        "response_count": attempted_count,
                        "correct_count": correct_count,
                    })
                    
                    if question_count > 0:
                        accuracy += correct_count
                        num_questions += question_count

                if num_questions > 0:
                    accuracy = accuracy / num_questions
                    accuracy = f"{accuracy * 100:.2f}"
                else:
                    accuracy = "N/A"

            # Construction and sending of email
            msg = Message("Monthly report from Quake",sender="jakyn@gmail.com",recipients=[user.email])
            # Note: Need to tidy up the HTML template
            msg.html = render_template("./report.html",user_name = user.name, no_quizes = len(quiz_set), quizes = quizes, accuracy = accuracy)
            conn.send(msg)

@celery.task()
def triggeredFullReport(uid):
    """
        Triggered task #1 - Generate a summary of all quiz attempts (all-time) by given
        user in a csv format and store the file on the server. Then notify the user by
        sending an email to inform them of completion of task.

        Trigger: User submits a request for summary
    """

    # Checking for existence of user!
    user = User.query.filter(User.is_admin == 0, User.id == uid).scalar()
    if user is None:
        return

    # Only querying quizes from the past (before current datetime)
    current_date = datetime.now()
    quizes = db.session.query(Quiz)
    quizes = quizes.join(Quiz.chapter).join(Chapter.subject).join(Subject.user)
    quizes = quizes.filter(User.id == user.id).filter(Quiz.dated < current_date)

    base_path = os.getcwd()
    filename = os.path.join(base_path,'api','static',f'report_{user.id}.csv')
    with open(filename,"w") as f:
        f.write("Quiz_ID,Correct,Attempted,No_Of_Questions,Accuracy\n")
        for quiz in quizes:
            score = Score.query.filter(Score.user_id == uid, Score.quiz_id == quiz.id).scalar()
            if score:
                if score.question_count > 0:
                    accuracy = score.correct_count / score.question_count
                    accuracy = f"{accuracy:.2f}"
                else:
                    accuracy = 0
                line = f"{quiz.id},{score.correct_count},{score.attempted_count},{score.question_count},{accuracy}"
                line += "\n"
                f.write(line)
                continue
            
            score = Score.query.filter(Score.user_id == user.id, Score.quiz_id == quiz.id).scalar()
            if score is None:                    
                question_count = quiz.questions.count()
                attempted_count, correct_count = recompute_score_one(quiz.id,user.id)
                score = Score(user_id = user.id, quiz_id = quiz.id, attempted_count = attempted_count, question_count = question_count, correct_count = correct_count)
                db.session.add(score)
                db.session.commit()

            if score.question_count > 0:
                accuracy = score.correct_count / score.question_count
                accuracy = f"{accuracy:.2f}"
            else:
                accuracy = "N/A"

            line = f"{quiz.id},{score.correct_count},{score.attempted_count},{score.question_count},{accuracy}"
            line += "\n"
            f.write(line)
    
    # Note: Need to tidy up the HTML template
    # Sending email notification when done!
    msg = Message("Attempt summary report generated!", sender="jakyn@gmail.com", recipients = [user.email])
    html_body = """
        <html>
            <head>
                <title>
                    Attempt summary report generated!
                </title>
            </head>
            <body>
                <p>
                    Your request for an attemt summary has been processed and your results are waiting for you!
                    <br>
                    Simply login and proceed to your summary page! Happy quizzing!
                </p>
            </body>
        </html>
    """
    msg.html = html_body
    mail.send(msg)

# Scheduler for periodic tasks
@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Periodic task #1
    sender.add_periodic_task(
        crontab(hour=0, minute=1),
        scheduledDailyReminder.s(),
    )

    # Periodic task #2
    sender.add_periodic_task(
        crontab(day_of_month=1),
        scheduledMonthlyReport.s()
    )