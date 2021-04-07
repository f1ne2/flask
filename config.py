import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = \
        "postgres://btkuhnvbxdcaxh:29feef89097b7c5db68a3e6d839ba08fab9e0037310ec1fee4271f824214c269@ec" \
        "2-54-235-108-217.compute-1.amazonaws.com:5432/de3p09926ksgnj"
    # os.environ.get("POSTGRE_SQL") or \
                              # 'postgresql://postgres:SNekH2233@localhost:5432/quiz'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
