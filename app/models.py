from app import app
from app import db


class Categories(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(64), nullable=False)
    categories = db.relationship("Questions", backref="quest", lazy='dynamic')

    def __repr__(self) -> str:
        return '{}'.format(self.category_name)


class Questions(db.Model):
    category_id = db.Column(db.Integer,
                            db.ForeignKey('categories.category_id'))
    question = db.Column(db.String(140), nullable=False)
    question_id = db.Column(db.Integer, primary_key=True)
    questions = db.relationship("Answers", backref="answ", lazy='dynamic')

    def __repr__(self) -> str:
        return '{}'.format(self.question)


class Answers(db.Model):
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    answer = db.Column(db.String, nullable=False)
    answer_id = db.Column(db.Integer, primary_key=True)
    right_answer = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return '{}'.format(self.answer)
