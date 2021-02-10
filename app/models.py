from app import db
from typing import List


class Categories(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(64), nullable=False)
    categories = db.relationship("Questions", backref="quest", lazy='dynamic')

    def __repr__(self) -> str:
        return '{}'.format(self.category_name)

    def put_category(self, category_id: int, category_name: str) -> None:
        note = Categories(category_id=category_id, category_name=category_name)
        db.session.add(note)
        db.session.commit()

    def get_all_table(self) -> List[list]:
        result = db.session.query(Categories).all()
        return [[element.category_id, element.category_name] for element in
                result]

    def delete_note(self, category_id: int) -> None:
        delt = db.session.query(Categories).filter_by\
            (category_id=category_id).one()
        db.session.delete(delt)
        db.session.commit()

    def to_json(self):
        json_category = {"Category_id": self.category_id,
                         "Category_name": self.category_name}
        return json_category

    def check_exist_category(self, category_id: int, category_name: str) -> \
            bool:
        arr = db.session.query(Categories).all()
        arr_id = [item.category_id for item in arr]
        arr_name = [item.category_name for item in arr]
        if category_id in arr_id or category_name in arr_name:
            return True
        return False


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
