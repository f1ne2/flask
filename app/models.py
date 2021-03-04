from app import db
from typing import List


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)


class Categories(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(64), nullable=False, unique=True)
    questions = db.relationship("Questions", backref="quest", lazy='dynamic')

    def __repr__(self) -> str:
        return '{}'.format(self.category_name)

    @staticmethod
    def add(category_name: str) -> None:
        category = Categories(category_name=category_name)
        db.session.add(category)
        db.session.commit()

    @staticmethod
    def get_categories() -> List[list]:
        categories = db.session.query(Categories).all()
        return [[item.category_id, item.category_name] for item in
                categories]

    @staticmethod
    def delete_note(category_id: int) -> None:
        delete = db.session.query(Categories).filter_by \
            (category_id=category_id).one()
        db.session.delete(delete)
        db.session.commit()

    def to_json(self):
        json_category = {"Category_id": self.category_id,
                         "Category_name": self.category_name}
        return json_category

    @staticmethod
    def edit(category_name: str, id: int) -> None:
        Categories.query.filter_by(category_id=id).update \
            (dict(category_name=category_name))
        db.session.commit()


class Questions(db.Model):
    category_id = db.Column(db.Integer,
                            db.ForeignKey('categories.category_id'))
    question = db.Column(db.String(140), nullable=False, unique=True)
    question_id = db.Column(db.Integer, primary_key=True)
    answers = db.relationship("Answers", backref="questions", lazy='dynamic')

    def __repr__(self) -> str:
        return '{}'.format(self.question)

    def __eq__(self, other):
        return self.question == other.question and self.category_id == \
               other.category_id and self.question_id == other.question_id


class Answers(db.Model):
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    answer = db.Column(db.String, nullable=False)
    answer_id = db.Column(db.Integer, primary_key=True)
    right_answer = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return '{}'.format(self.answer)

    def __eq__(self, other):
        return self.answer == other.answer and self.answer_id == \
               other.answer_id and self.question_id == other.question_id and \
               self.right_answer == other.right_answer
