import unittest
from app.models import Categories, Questions, Answers
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_models.db'
engine = create_engine('sqlite:///test_models.db')
connection = engine.connect()
metadata = MetaData()


class TestCategories(unittest.TestCase):
    def setUp(self) -> None:
        self.category = Table('Categories', metadata,
                              Column('category_id', Integer(),
                                     primary_key=True),
                              Column('category_name',
                                     String(45), nullable=False))
        metadata.create_all(engine)

    def test_categories(self) -> None:
        db = SQLAlchemy(app)
        self.note = Categories(category_id=1, category_name='Nature')
        db.session.add(self.note)
        db.session.commit()
        self.res = db.session.query(Categories).all()
        self.assertEqual(self.res[0].category_name, "Nature")


class TestQuestions(unittest.TestCase):
    def setUp(self) -> None:
        self.question = Table('Questions', metadata,
                              Column('category_id', Integer(),
                                     ForeignKey(Categories.category_id)),
                              Column('question', String(120),
                                     nullable=False),
                              Column('question_id', Integer(),
                                     primary_key=True))
        metadata.create_all(engine)

    def test_questions(self):
        db = SQLAlchemy(app)
        self.note = Questions(category_id=1, question='What? Where? When?',
                              question_id=1)
        db.session.add(self.note)
        db.session.commit()
        self.res = db.session.query(Questions).all()
        self.note = Questions(category_id=2, question='234',
                              question_id=2)
        db.session.add(self.note)
        db.session.commit()
        del_id = db.session.query(Questions).all()
        print(del_id)
        lis = []
        for i in range(len(del_id)):
            lis.append(del_id[i].category_id)
            lis.append(del_id[i].question)
            lis.append(del_id[i].question_id)
        print(lis)
        self.assertEqual(self.res[0].question, 'What? Where? When?')


class TestAnswers(unittest.TestCase):
    def setUp(self) -> None:
        self.answer = Table('Answers', metadata,
                            Column('question_id', Integer(),
                                   ForeignKey(Questions.question_id)),
                            Column('answer', String(120),
                                   nullable=False),
                            Column('answer_id', Integer(),
                                   primary_key=True),
                            Column('right_answer', String(45), nullable=False))
        metadata.create_all(engine)

    def test_answers(self):
        db = SQLAlchemy(app)
        self.note = Answers(question_id=1, answer='Play', answer_id=1,
                            right_answer='YES')
        db.session.add(self.note)
        db.session.commit()
        self.res = db.session.query(Answers).all()
        self.assertEqual(self.res[0].answer, 'Play')
