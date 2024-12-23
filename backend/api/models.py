from api.database import db

registered = db.Table("registered",
    db.Column("user_id",db.Integer,db.ForeignKey('users.id'), primary_key = True),
    db.Column("subject_id",db.Integer,db.ForeignKey('subjects.id'), primary_key = True),
)

problem = db.Table("problem",
    db.Column("question_id",db.Integer,db.ForeignKey('questions.id'), primary_key = True),
    db.Column("quiz_id",db.Integer,db.ForeignKey('quizes.id'), primary_key = True),
)

class User(db.Model):
    """
        User model representing authorised users and admin.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(40),unique = True, nullable = False)
    email = db.Column(db.String(128),unique = True, nullable = False)
    password = db.Column(db.String(64), nullable = False)
    is_admin = db.Column(db.Integer, default = 0, nullable = False)

    subjects = db.relationship('Subject', secondary = registered, backref = 'users')
    responses = db.relationship('Response', backref="user")
    scores = db.relationship('Score', backref = 'user')

class Subject(db.Model):
    """
        Subject model representing a certain field of study.
    """
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40),unique = True, nullable = False)
    description = db.Column(db.String(128))
    credits = db.Column(db.Integer, nullable = False)

    chapters = db.relationship('Chapter', backref='subject')

class Chapter(db.Model):
    """
        Chapter model representing a topic of a particular field.
    """
    __tablename__ = "chapters"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(40),unique = True, nullable = False)
    description = db.Column(db.String(128))
    order = db.Column(db.Integer)

    quizes = db.relationship('Quiz', backref = "chapter")
    questions = db.relationship("Question", backref = "chapter")

class Quiz(db.Model):
    """
        Quiz model representing a test of some chapter.
    """
    __tablename__ = "quizes"

    id = db.Column(db.Integer, primary_key = True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable = False)
    dated = db.Column(db.DateTime, nullable = False)
    duration = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String(128))

    questions = db.relationship('Question', secondary = problem, backref = 'quizes')
    responses = db.relationship('Response', backref='quiz')
    scores = db.relationship('Score', backref = 'quiz')

class Question(db.Model):
    """
        Question model representing a MCQ on some chapter.
    """
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key = True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable = False)
    description = db.Column(db.String(512), nullable = False)
    options = db.Column(db.String(256), nullable = False)
    correct = db.Column(db.Integer, nullable = False)
    marks = db.Column(db.Integer, nullable = False)

    responses = db.relationship('Response', backref='quiz')

class Response(db.Model):
    """
        Response model representing an answer to a question in a quiz by some user.
    """ 
    __tablename__ = "responses"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizes.id'), nullable = False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable = False)
    marked = db.Column(db.Integer, nullable = False)
    answered_at = db.Column(db.DateTime, nullable = False)

class Score(db.Model):
    """
        Score model representing the result of a quiz given by some user.
    """
    __tablename__ = "scores"

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizes.id'), nullable = False)
    total = db.Column(db.Integer, nullable = False)
    start_time = db.Column(db.DateTime, nullable = False)
    end_time = db.Column(db.DateTime, nullable = False)
