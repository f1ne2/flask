from app import app
from app import db
from app.models import Users

from flask import jsonify, wrappers, request, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

import jwt
import datetime


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
            current_user = [data['id'], data['admin']]

            if not current_user[1]:
                return jsonify({'message': 'Cannot perform that function!'})

        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated


@app.route('/login')
def login() -> wrappers.Response:
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = Users.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id': user.id, 'admin': user.admin,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)},
                           app.config['SECRET_KEY'])

        return jsonify({'token': token})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@app.route('/user', methods=['POST'])
def create_user() -> wrappers.Response:
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = Users(name=data['name'], password=hashed_password, admin=False)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})


@app.route('/user/<int:id>', methods=['PUT'])
@token_required
def promote_user(id: int) -> wrappers.Response:
    user = Users.query.filter_by(id=id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message': 'The user has been promoted!'})


@app.route('/user', methods=['GET'])
@token_required
def get_all_users() -> wrappers.Response:
    users = Users.query.all()
    output = []

    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users': output})


@app.route('/user/<int:id>', methods=['GET'])
@token_required
def get_one_user(id: int) -> wrappers.Response:
    user = Users.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message': 'No user found!'})

    user_data = {}
    user_data['id'] = user.id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user': user_data})


@app.route('/user/<int:id>', methods=['DELETE'])
@token_required
def delete_user(id: int) -> wrappers.Response:
    user = Users.query.filter_by(id=id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'The user has been deleted!'})
