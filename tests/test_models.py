import unittest
from flask import *
from flask_sqlalchemy import *
from typing import Callable


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///D:/Git/flask/tests/test_models.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class MySQLAlchemy(SQLAlchemy):
    Column: Callable
    String: Callable
    Integer: Callable
    relationship: Callable
    ForeignKey: Callable


db = MySQLAlchemy(app)
db.create_all()


class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer(), primary_key=True)
    category_name = db.Column(db.String(64), nullable=False)
    db.create_all()


class Questions(db.Model):
    __tablename__ = 'questions'
    category_id = db.Column(db.Integer,
                            db.ForeignKey('categories.id'))
    question = db.Column(db.String(140), nullable=False)
    question_id = db.Column(db.Integer, primary_key=True)
    questions = db.relationship("Answers", backref="answ", lazy='dynamic')
    db.create_all()


class Answers(db.Model):
    __tablename__ = 'answers'
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    answer = db.Column(db.String, nullable=False)
    answer_id = db.Column(db.Integer, primary_key=True)
    right_answer = db.Column(db.String, nullable=False)
    db.create_all()


class TestCategories(unittest.TestCase):
    def test_categories(self) -> None:
        db.create_all()
        category = Categories(id=1, category_name='bla bla')
        db.session.add(category)
        db.session.commit()
        categories = db.session.query(Categories).all()
        self.assertEqual(categories[0].id, 1)
        self.assertEqual(categories[0].category_name, 'bla bla')

    def test_add(self) -> None:
        db.create_all()
        category = Categories(id=2, category_name="Countries")
        db.session.add(category)
        db.session.commit()
        categories = db.session.query(Categories).all()
        self.assertEqual(categories[0].category_name, 'Countries')
        self.assertEqual(categories[0].id, 2)

    def test_get_categories(self) -> None:
        db.create_all()
        note = Categories(id=2, category_name="Countries")
        db.session.add(note)
        db.session.commit()
        res = db.session.query(Categories).all()
        out = [[element.id, element.category_name] for element in res]
        self.assertEqual(out, [[2, 'Countries']])

    def test_delete_note(self) -> None:
        note = Categories(id=3, category_name="Oceans")
        db.session.add(note)
        note = Categories(id=2, category_name="Countries")
        db.session.add(note)
        db.session.commit()
        category_id = 3
        category = db.session.query(Categories).filter_by\
            (id=category_id).one()
        db.session.delete(category)
        db.session.commit()
        categories = db.session.query(Categories).all()
        out = [[element.id, element.category_name] for element in categories]
        self.assertEqual(out, [[2, 'Countries']])

    def test_to_json(self) -> None:
        category = Categories(id=2, category_name="Countries")
        db.session.add(category)
        db.session.commit()
        json_category = {"Category_id": category.id,
                         "Category_name": category.category_name}
        self.assertEqual(json_category, {"Category_id": 2,
                                         "Category_name": "Countries"})

    def test_check_exist_category(self) -> None:
        category = Categories(id=2, category_name="Countries")
        db.session.add(category)
        db.session.commit()
        category_1 = "Nature"
        category_2 = "Countries"
        categories = db.session.query(Categories).all()
        category_names = [item.category_name for item in categories]
        self.assertEqual(category_1 in category_names, False)
        self.assertEqual(category_2 in category_names, True)

    def test_edit(self) -> None:
        note = Categories(id=2, category_name="Countries")
        db.session.add(note)
        db.session.commit()
        category = db.session.query(Categories).filter_by(id=note.id).one()
        category.category_name = "Nature"
        db.session.add(category)
        db.session.commit()
        categories = db.session.query(Categories).all()
        out = [[element.id, element.category_name] for element in categories]
        self.assertEqual(out, [[2, 'Nature']])

    def tearDown(self) -> None:
        arr = db.session.query(Categories).all()
        db.session.delete(arr[0])
        db.session.commit()


class TestQuestions(unittest.TestCase):
    def test_questions(self) -> None:
        question = Questions(category_id=1, question='What? Where? When?',
                             question_id=1)
        db.session.add(question)
        db.session.commit()
        question = Questions(category_id=2, question='234', question_id=2)
        db.session.add(question)
        db.session.commit()
        questions = db.session.query(Questions).all()
        self.assertEqual(questions[1], question)


class TestAnswers(unittest.TestCase):
    def test_answers(self) -> None:
        db.create_all()
        answer = Answers(question_id=1, answer='Play', answer_id=1,
                       right_answer='YES')
        db.session.add(answer)
        db.session.commit()
        self.res = db.session.query(Answers).all()
        self.assertEqual(self.res[0], answer)


if __name__ == "__main__":
    unittest.main()
