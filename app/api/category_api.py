from app import app
from app.api.users_api import token_required
from app.models import Categories

from flask import jsonify, wrappers, request



@app.route('/')
def home_page():
    return 'Home page!'


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
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    category = request.form['data']
    try:
        Categories.add(category)
        return jsonify({"201 Created": "HTTP/1.1"})
    except:
        return jsonify({"403 Forbidden": "HTTP/1.1"})


@app.route('/category/<int:id>', methods=['DELETE'])
@token_required
def delete_category(current_user, id: int) -> wrappers.Response:
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    Categories.query.get_or_404(id)
    Categories.delete_note(id)
    return jsonify({"200 OK": "HTTP/1.1"})


@app.route('/category/<int:id>', methods=['PUT'])
@token_required
def edit_category(current_user, id: int) -> wrappers.Response:
    if not current_user.admin:
        return jsonify({'message': 'Cannot perform that function!'})

    Categories.query.get_or_404(id)
    try:
        Categories.edit(request.form['data'], id)
        return jsonify({"200 OK": "HTTP/1.1"})
    except:
        return jsonify({"403 Forbidden": "HTTP/1.1"})
