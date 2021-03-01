from flask import Flask, request, jsonify
from config import Config
from models import Users
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import jwt

from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models
from app.api import category_api

db.create_all()


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, app.config[Config.SECRET_KEY])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
            return f(current_user, *args, **kwargs)
        except:
            return jsonify({'message': 'token is invalid'})

    return decorator
