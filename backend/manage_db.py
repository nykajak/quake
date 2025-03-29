from api.models import *
from api import bcrypt
from api import db
from json import dumps,loads
from datetime import datetime


def make_file():
    userin = input("Overwrite save? (y/n) ")
    if userin.lower() != "y":
        return
    
    with open("database.json", "w") as f:
        # Construct snapshot
        d = {}

        # Fetching subject data
        d["subjects"] = []
        subjects = Subject.query.all()
        for u in subjects:
            d["subjects"].append(u.serialise())


        # Fetching chapter data
        d["chapters"] = []
        chapters = Chapter.query.all()
        for u in chapters:
            x = u.serialise()
            x["subject"] = {"id": x["subject"]['id']}
            d["chapters"].append(x)


        # Fetching quiz data
        d["quizes"] = []
        quizes = Quiz.query.all()
        for u in quizes:
            x = u.serialise(required=("chapter"))
            x["chapter"] = {"id": x["chapter"]['id']}
            d["quizes"].append(x)

        
        # Fetching question data
        d["questions"] = []
        questions = Question.query.all()
        for u in questions:
            x = u.serialise(required=("chapter"))
            x["chapter"] = {"id": x["chapter"]['id']}
            d["questions"].append(x)

        # Fetching response data
        d["responses"] = []
        responses = Response.query.all()
        for u in responses:
            x = u.serialise(required=("user","question","quiz"))
            x["user"] = {"id": x["user"]['id']}
            x["question"] = {"id": x["question"]['id']}
            x["quiz"] = {"id": x["quiz"]['id']}
            d["responses"].append(x)
        
        # Fetching registered data
        d["registered"] = []
        registered = {u.id: tuple([x.id for x in u.subjects]) for u in User.query.all()}
        d["registered"] = registered


        # Fetching problem data
        d["problem"] = []
        problems = {q.id: tuple([x.id for x in q.questions]) for q in Quiz.query.all()}
        d["problem"] = problems

        # Fetching score data
        d["scores"] = []
        for s in Score.query.all():
            d["scores"].append(s.serialise(required = ('user','quiz')))

        # Writing to file
        f.writelines(dumps(d))

def add_users():
    users = [
        User(name = "Jakyn", password = bcrypt.generate_password_hash("654321"), email = "jakyn@gmail.com", is_admin = 1),
        User(name = "beautifulmouse476", password = bcrypt.generate_password_hash("doggie"), email = "vicente.torres@example.com"),
        User(name = "yellowcat882", password = bcrypt.generate_password_hash("penguin"), email = "justine.ma@example.com"),
        User(name = "brownostrich737", password = bcrypt.generate_password_hash("xhai"), email = "sonke.schwinn@example.com"),
        User(name = "blackduck796", password = bcrypt.generate_password_hash("sebastian1"), email = "juliocesar.urias@example.com"),
        User(name = "purpleswan273", password = bcrypt.generate_password_hash("2222DJ"), email = "andrijana.malesevic@example.com"),
        User(name = "greenrabbit317", password = bcrypt.generate_password_hash("blueberry"), email = "fatima.delgado@example.com"),
        User(name = "organiclion897", password = bcrypt.generate_password_hash("19821"), email = "olivia.sanchez@example.com"),
        User(name = "tinyostrich816", password = bcrypt.generate_password_hash("arcane"), email = "adryn.khwty@example.com"),
        User(name = "brownfrog618", password = bcrypt.generate_password_hash("espresso"), email = "sara.soto@example.com"),
    ]

    for u in users:
        db.session.add(u)

    db.session.commit()
    print("Finished adding users!")

def add_subjects(content):
    for s in content["subjects"]:
        obj = Subject(
            id = s["id"],
            name = s["name"],
            description = s["description"],
        )
        db.session.add(obj)

    db.session.commit()
    print("Finished adding subjects!")

def add_chapters(content):
    for c in content["chapters"]:
        obj = Chapter(
            id = c["id"],
            name = c["name"],
            description = c["description"],
            subject_id = c["subject"]["id"]
        )
        db.session.add(obj)

    db.session.commit()
    print("Finished adding chapters!")

def add_questions(content):
    for q in content["questions"]:
        obj = Question(
            id = q["id"],
            description = q["description"],
            options = "#".join(q["options"]),
            correct = q["correct"],
            chapter_id = q["chapter"]["id"]
        )

        db.session.add(obj)

    db.session.commit()
    print("Finished adding questions!")

def add_quizes(content):
    for q in content["quizes"]:
        obj = Quiz(
            id = q["id"],
            description = q["description"],
            duration = q["duration"],
            chapter_id = q["chapter"]["id"],
            dated = datetime(
                day = int(q["dated"]["day"]),
                month = int(q["dated"]["month"]),
                year = int(q["dated"]["year"]),
                hour = int(q["dated"]["hour"]),
                minute = int(q["dated"]["minute"]),
            )
        )

        db.session.add(obj)

    db.session.commit()
    print("Finished adding quizes!")

def add_registered(content):
    for uid,sids in content["registered"].items():
        u = User.query.filter(User.id == int(uid)).scalar()
        for sid in sids:
            s = Subject.query.filter(Subject.id == int(sid)).scalar()
            if s is not None:
                u.subjects.append(s)

    db.session.commit()
    print("Finished adding registered!")

def add_problem(content):
    for quiz_id,question_ids in content["problem"].items():
        quiz = Quiz.query.filter(Quiz.id == int(quiz_id)).scalar()
        for question_id in question_ids:
            question = Question.query.filter(Question.id == int(question_id)).scalar()
            quiz.questions.append(question)

    db.session.commit()
    print("Finished adding problem!")

def add_responses(content):
    for r in content["responses"]:
        obj = Response(
            marked = r["marked"],
            user_id = r["user"]["id"],
            quiz_id = r["quiz"]["id"],
            question_id = r["question"]["id"],
            answered_at = datetime(
                day = int(r["dated"]["day"]),
                month = int(r["dated"]["month"]),
                year = int(r["dated"]["year"]),
                hour = int(r["dated"]["hour"]),
                minute = int(r["dated"]["minute"]),
            )
        )

        db.session.add(obj)

    db.session.commit()
    print("Finished adding responses!")

def add_scores(content):
    for s in content["scores"]:
        obj = Score(
            correct_count = s["correct_count"],
            attempted_count = s["attempted_count"],
            question_count = s["question_count"],
            user_id = s["user"]["id"],
            quiz_id = s["quiz"]["id"]
        )

        db.session.add(obj)

    db.session.commit()
    print("Finished adding scores!")

def make_db():

    userin = input("Remake database? (y/n) ")
    if userin.lower() != "y":
        return
    
    db.drop_all()
    db.create_all()

    with open("database.json", "r") as f:
        content = f.read()

    content = loads(content)
    add_users()
    add_subjects(content)
    add_chapters(content)
    add_questions(content)
    add_quizes(content)
    add_registered(content)
    add_problem(content)
    add_responses(content)
    add_scores(content)

print("Enter 1 to save database")
print("Enter 2 to remake databse")
userin = input("Enter action ")

if userin == "1":
    make_file()

elif userin == "2":
    make_db()
