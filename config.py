import os


class Config(object):
    SECRET_KEY = 'you-will-never-guess'
    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get("POSTGRE_SQL") or \
                              'postgresql://postgres:admin@localhost:5432/quiz'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
