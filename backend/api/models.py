from api.database import db
import datetime

# Registered relation to check if user registered for a particular course. (many to many)
registered = db.Table("registered",
    db.Column("user_id",db.Integer,db.ForeignKey('users.id'), primary_key = True),
    db.Column("subject_id",db.Integer,db.ForeignKey('subjects.id'), primary_key = True),
)

# Problem relation to check if quiz contains some specific question. (many to many)
problem = db.Table("problem",
    db.Column("question_id",db.Integer,db.ForeignKey('questions.id'), primary_key = True),
    db.Column("quiz_id",db.Integer,db.ForeignKey('quizes.id'), primary_key = True),
)

class User(db.Model):
    """
        User model representing users - both normal and admin.
    """
    __tablename__ = "users"

    # Attributes
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(40),unique = True, nullable = False)
    email = db.Column(db.String(128),unique = True, nullable = False)
    password = db.Column(db.String(128), nullable = False)
    is_admin = db.Column(db.Integer, default = 0, nullable = False)

    # Relationships
    
    # To Subject through registered - denoting enrollment - many to many
    subjects = db.relationship('Subject', secondary = registered, back_populates='users', lazy='dynamic')

    # To Response - denoting ownership of response - one to many
    responses = db.relationship('Response', back_populates="user", lazy='dynamic')

    # To Score - denoting ownership of score - one to many
    scores = db.relationship('Score', back_populates = 'user', lazy='dynamic')

    def serialise(self,required = ()):
        """
            Serialise method provided to return a json serialisable representation of user.
            Does not allow serialisation of password or is_admin.
        """
        res = {
            "id" : self.id,
            "name": self.name,
            "email": self.email,
        }

        if len(required) == 0:
            return res
        
        if "subjects" in required:
            res["subjects"] = [subject.serialise() for subject in self.subjects]
        
        if "responses" in required:
            res["responses"] = [response.serialise() for response in self.responses]

        if "scores" in required:
            res["scores"] = [score.serialise() for score in self.scores]

        return res

class Subject(db.Model):
    """
        Subject model representing a certain field of study.
    """
    __tablename__ = "subjects"

    # Attributes
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80),unique = True, nullable = False)
    description = db.Column(db.String(128))

    # Relationships

    # To User through registered - denoting enrollment - many to many
    users = db.relationship('User', secondary = registered, back_populates='subjects', lazy='dynamic')

    # To Chapter - denoting children - one to many
    chapters = db.relationship('Chapter', back_populates='subject', lazy='dynamic', cascade="all, delete")

    def serialise(self,required = ()):
        """
            Serialise method provided to return a json serialisable representation of subject.
        """
        res = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

        if len(required) == 0:
            return res

        if "chapters" in required:
            res["chapters"] = [chapter.serialise() for chapter in self.chapters]
        
        if "users" in required:
            res["users"] = [user.serialise() for user in self.users]

        return res

class Chapter(db.Model):
    """
        Chapter model representing a topic of a particular field.
    """
    __tablename__ = "chapters"

    # Attributes
    id = db.Column(db.Integer, primary_key = True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable = False)
    name = db.Column(db.String(80), nullable = False)
    description = db.Column(db.String(128))

    # Relationships

    # To Subject - denoting container - many to one
    subject = db.relationship('Subject', back_populates='chapters')

    # To Quiz - denoting children - one to many
    quizes = db.relationship('Quiz', back_populates = "chapter", lazy='dynamic', cascade="all, delete")

    # To Question - denoting children - one to many
    questions = db.relationship("Question", back_populates = "chapter", lazy='dynamic', cascade="all, delete")

    def serialise(self,required = ()):
        """
            Serialise method provided to return a json serialisable representation of chapter.
        """
        res = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

        res["subject"] = self.subject.serialise()
        if len(required) == 0:
            return res

        if "quizes" in required:
            res["quizes"] = [quiz.serialise() for quiz in self.quizes]

        if "questions" in required:
            res["questions"] = [question.serialise() for question in self.questions]

        return res

class Quiz(db.Model):
    """
        Quiz model representing a test of some chapter.
    """
    __tablename__ = "quizes"

    # Attributes
    id = db.Column(db.Integer, primary_key = True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable = False)
    dated = db.Column(db.DateTime, nullable = False)
    duration = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String(128),nullable=False)

    # Relationships

    # To Chapter - denoting parent/container - many to one
    chapter = db.relationship('Chapter', back_populates = "quizes")

    # To Score - denoting performance metric - one to many
    scores = db.relationship('Score', back_populates = 'quiz', lazy='dynamic', cascade="all, delete")

    # To Response - denoting specific attempt details - one to many
    responses = db.relationship('Response', back_populates='quiz', lazy='dynamic', cascade="all, delete")

    # To Question - denoting membership in quiz - many to many
    questions = db.relationship('Question', secondary = problem, back_populates = 'quizes', lazy='dynamic')

    def serialise(self,required = ()):
        """
            Serialise method provided to return a json serialisable representation of quiz.
        """
        res = {
            "id": self.id,
            "dated": {
                "day":f"{self.dated.day}",
                "month":f"{self.dated.month}",
                "year":f"{self.dated.year}",
                "hour":f"{self.dated.hour:0>2}",
                "minute":f"{self.dated.minute:0>2}",
            },
            "duration": self.duration,
            "description": self.description
        }

        if len(required) == 0:
            return res

        if "chapter" in required:
            res["chapter"] = self.chapter.serialise()

        if "questions" in required:
            res["questions"] = [question.serialise() for question in self.questions]
        
        if "responses" in required:
            res["responses"] = [response.serialise() for response in self.responses]

        if "scores" in required:
            res["scores"] = [score.serialise() for score in self.scores]

        return res

class Question(db.Model):
    """
        Question model representing a MCQ on some chapter.
    """
    __tablename__ = "questions"

    # Attributes
    id = db.Column(db.Integer, primary_key = True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable = False)
    description = db.Column(db.String(512), nullable = False)
    options = db.Column(db.String(256), nullable = False)
    correct = db.Column(db.Integer, nullable = False)

    # Relationships

    # To Chapter - denoting parent/container - many to one
    chapter = db.relationship("Chapter", back_populates = "questions")
    
    # To Quiz - denoting being a part of - many to many
    quizes = db.relationship('Quiz', secondary = problem, back_populates = 'questions', lazy='dynamic')

    # To Response - denoting target of response - one to many
    responses = db.relationship('Response', back_populates='question', lazy='dynamic',cascade="all, delete")

    def serialise(self,required = ()):
        """
            Serialise method provided to return a json serialisable representation of question.
        """
        res = {
            "id": self.id,
            "description": self.description,
            "options": self.options.split("#"),
            "correct": self.correct
        }

        if len(required) == 0:
            return res
        
        if "unsafe" in required:
            del res["correct"]

        if "chapter" in required:
            res["chapter"] = self.chapter.serialise()
        
        if "responses" in required:
            res["responses"] = [response.serialise() for response in self.responses]
        return res

class Response(db.Model):
    """
        Response model representing an answer to a question in a quiz by some user.
    """ 
    __tablename__ = "responses"

    # Attributes
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizes.id'), primary_key = True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key = True)
    marked = db.Column(db.Integer, nullable = False)
    answered_at = db.Column(db.DateTime, nullable = False)

    # Relationships

    # To User - denoting attempter - many to one
    user = db.relationship('User', back_populates="responses")

    # To Quiz - denoting attempt occasion - many to one
    quiz = db.relationship('Quiz', back_populates="responses")

    # To Question - denoting attempt target - many to one
    question = db.relationship('Question', back_populates="responses")

    def serialise(self,required = ()):
        """
            Serialise method provided to return a json serialisable representation of response.
        """
        res = {
            "marked": self.marked,
            "dated": {
                "day":f"{self.answered_at.day}",
                "month":f"{self.answered_at.month}",
                "year":f"{self.answered_at.year}",
                "hour":f"{self.answered_at.hour:0>2}",
                "minute":f"{self.answered_at.minute:0>2}",
            },
        }

        if len(required) == 0:
            return res

        if "user" in required:
            res["user"] = self.user.serialise()
        
        if "question" in required:
            res["question"] = self.question.serialise(required = ('chapter'))

        if "quiz" in required:
            res["quiz"] = self.quiz.serialise(required = ('chapter'))

        return res

class Score(db.Model):
    """
        Score model representing the result of a quiz given by some user.
    """
    __tablename__ = "scores"

    
    # Attributes
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizes.id'), primary_key = True)
    correct_count = db.Column(db.Integer, nullable = False)
    attempted_count = db.Column(db.Integer, nullable = False)
    question_count = db.Column(db.Integer, nullable = False)

    # Relationships
    
    # To User - denoting attempter - many to one
    user = db.relationship('User', back_populates = 'scores')
    
    # To Quiz - denoting attempt occasion - many to one
    quiz = db.relationship('Quiz', back_populates = 'scores')

    def serialise(self,required = ()):
        """
            Serialise method provided to return a json serialisable representation of score.
        """
        res = {
            "correct_count": self.correct_count,
            "attempted_count": self.attempted_count,
            "question_count":self.question_count
        }

        if len(required) == 0:
            return res
        
        if "user" in required:
            res["user"] = self.user.serialise()

        if "quiz" in required:
            res["quiz"] = self.quiz.serialise()

        return res
    
class Requested(db.Model):
    """
        Requested model that represents User sending a request to enroll 
    """

    __tablename__ = "requested"

    # Attributes
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key = True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), primary_key = True)
    dated = db.Column(db.DateTime, nullable = False, default = datetime.datetime.now())

    # Relationships
    
    # To Subject - denoting target of request - one to one
    subject = db.relationship('Subject', backref="requested")
    
    # To User - denoting issuer of request - one to one
    user = db.relationship('User', backref="requested")

    def serialise(self,required = ()):
         """
            Serialise method provided to return a json serialisable representation of requested.
        """
         res = {
            "user_id": self.user_id,
            "subject_id": self.subject_id,
            "dated": {
                "day":f"{self.dated.day}",
                "month":f"{self.dated.month}",
                "year":f"{self.dated.year}",
                "hour":f"{self.dated.hour:0>2}",
                "minute":f"{self.dated.minute:0>2}",
            },
        }
         
         return res