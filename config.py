import os


class Config(object):
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get("POSTGRE_SQL") or \
                              'postgresql://postgres:admin@localhost:5432/quiz'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
