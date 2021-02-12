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
    def test_categories(self):
        db.create_all()
        note = Categories(id=1, category_name='bla bla')
        db.session.add(note)
        db.session.commit()
        res = db.session.query(Categories).all()
        self.assertEqual(res[0].id, 1)
        self.assertEqual(res[0].category_name, 'bla bla')

    def test_add(self):
        db.create_all()
        note = Categories(id=2, category_name="Countries")
        db.session.add(note)
        db.session.commit()
        res = db.session.query(Categories).all()
        self.assertEqual(res[0].category_name, 'Countries')
        self.assertEqual(res[0].id, 2)

    def test_get_categories(self):
        db.create_all()
        note = Categories(id=2, category_name="Countries")
        db.session.add(note)
        db.session.commit()
        res = db.session.query(Categories).all()
        out = [[element.id, element.category_name] for element in res]
        self.assertEqual(out, [[2, 'Countries']])

    def test_delete_note(self):
        note = Categories(id=3, category_name="Oceans")
        db.session.add(note)
        note = Categories(id=2, category_name="Countries")
        db.session.add(note)
        db.session.commit()
        category_id = 3
        delt = db.session.query(Categories).filter_by\
            (id=category_id).one()
        db.session.delete(delt)
        db.session.commit()
        res = db.session.query(Categories).all()
        out = [[element.id, element.category_name] for element in res]
        self.assertEqual(out, [[2, 'Countries']])

    def test_to_json(self):
        note = Categories(id=2, category_name="Countries")
        db.session.add(note)
        db.session.commit()
        json_category = {"Category_id": note.id,
                         "Category_name": note.category_name}
        self.assertEqual(json_category, {"Category_id": 2,
                                         "Category_name": "Countries"})

    def test_check_exist_category(self):
        note = Categories(id=2, category_name="Countries")
        db.session.add(note)
        db.session.commit()
        category_1 = "Nature"
        category_2 = "Countries"
        arr = db.session.query(Categories).all()
        arr_name = [item.category_name for item in arr]
        self.assertEqual(category_1 in arr_name, False)
        self.assertEqual(category_2 in arr_name, True)

    def test_edit(self):
        note = Categories(id=2, category_name="Countries")
        db.session.add(note)
        db.session.commit()
        cat = db.session.query(Categories).filter_by(id=note.id).one()
        cat.category_name = "Nature"
        db.session.add(cat)
        db.session.commit()
        res = db.session.query(Categories).all()
        out = [[element.id, element.category_name] for element in res]
        self.assertEqual(out, [[2, 'Nature']])

    def tearDown(self) -> None:
        arr = db.session.query(Categories).all()
        db.session.delete(arr[0])
        db.session.commit()


class TestQuestions(unittest.TestCase):
    def test_questions(self) -> None:
        note = Questions(category_id=1, question='What? Where? When?',
                         question_id=1)
        db.session.add(note)
        db.session.commit()
        self.res = db.session.query(Questions).all()
        self.note = Questions(category_id=2, question='234',
                              question_id=2)
        db.session.add(self.note)
        db.session.commit()
        del_id = db.session.query(Questions).all()
        lis = []
        for i in range(len(del_id)):
            lis.append(del_id[i].category_id)
            lis.append(del_id[i].question)
            lis.append(del_id[i].question_id)
        self.assertEqual(self.res[0].question, 'What? Where? When?')


class TestAnswers(unittest.TestCase):
    def test_answers(self) -> None:
        db.create_all()
        note = Answers(question_id=1, answer='Play', answer_id=1,
                       right_answer='YES')
        db.session.add(note)
        db.session.commit()
        self.res = db.session.query(Answers).all()
        self.assertEqual(self.res[0].answer, 'Play')


if __name__ == "__main__":
    unittest.main()
