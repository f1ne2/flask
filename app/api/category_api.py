from app import app
from app import db
from flask import jsonify, wrappers, request, make_response
from app.models import Categories, Users
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.encode().decode(token, app.config['SECRET_KEY'])
            current_user = Users.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/')
def home_page():
    return 'Home page!'


@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = Users(name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created!'})


@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    if not current_user.admin: return jsonify({'message': 'Cannot perform that function!'})

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
def get_one_user(id: int, current_user):
    if not current_user.admin: return jsonify({'message': 'Cannot perform that function!'})

    user = Users.query.filter_by(id=id).first()
    if not user:
        return jsonify({'message': 'No user found!'})

    user_data = {}
    user_data['id'] = user.id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user': user_data})


@app.route('/user/<int:id>', methods=['PUT'])
@token_required
def promote_user(id: int, current_user):
    if not current_user.admin: return jsonify({'message': 'Cannot perform that function!'})
    user = Users.query.filter_by(id=id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message': 'The user has been promoted!'})


@app.route('/user/<int:id>', methods=['DELETE'])
@token_required
def delete_user(id: int, current_user):
    if not current_user.admin: return jsonify({'message': 'Cannot perform that function!'})
    user = Users.query.filter_by(id=id).first()

    if not user:
        return jsonify({'message': 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'The user has been deleted!'})


@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = Users.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id': user.id,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10)},
                           app.config['SECRET_KEY'])
        #token = jwt.encode({'id': user.id}, app.config['SECRET_KEY'])

        return jsonify({'token': token.encode().decode()})
        # return jsonify({'token': token.decode("utf-8")})
        # return jsonify({'token': token.encode("windows-1252").decode("utf-8")})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


# ___________________________________________________________________#
@app.route('/categories/', methods=['GET'])
def categories() -> wrappers.Response:
    return jsonify(dict(Categories.get_categories()))


@app.route('/category/<int:id>', methods=['GET'])
def get_category(id: int) -> wrappers.Response:
    category = Categories.query.get_or_404(id)
    return jsonify(category.to_json())


@app.route('/category/', methods=['POST'])
@token_required
def add_category(current_user) -> wrappers.Response:
    if not current_user.admin: return jsonify({'message': 'Cannot perform that function!'})
    category = request.form['data']
    try:
        Categories.add(category)
        return jsonify({"201 Created": "HTTP/1.1"})
    except:
        return jsonify({"403 Forbidden": "HTTP/1.1"})


@app.route('/category/<int:id>', methods=['DELETE'])
@token_required
def delete_category(id: int, current_user) -> wrappers.Response:
    if not current_user.admin: return jsonify({'message': 'Cannot perform that function!'})
    Categories.query.get_or_404(id)
    Categories.delete_note(id)
    return jsonify({"200 OK": "HTTP/1.1"})


@app.route('/category/<int:id>', methods=['PUT'])
# @token_required
def edit_category(id: int) -> wrappers.Response:
    Categories.query.get_or_404(id)
    try:
        Categories.edit(request.form['data'], id)
        return jsonify({"200 OK": "HTTP/1.1"})
    except:
        return jsonify({"403 Forbidden": "HTTP/1.1"})
