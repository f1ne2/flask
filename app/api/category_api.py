from app import app
from flask import jsonify, wrappers, request
from app.models import Categories


@app.route('/categories/', methods=['GET'])
def categories() -> wrappers.Response:
    return jsonify(dict(Categories.get_categories()))


@app.route('/category/<int:id>', methods=['GET'])
def get_category(id: int) -> wrappers.Response:
    category = Categories.query.get_or_404(id)
    return jsonify(category.to_json())


@app.route('/category/', methods=['POST'])
def add_category() -> wrappers.Response:
    category = request.form['data']
    if Categories.check_exist_category(category):
        return jsonify({"403 Forbidden": "HTTP/1.1"})
    Categories.add(category)
    return jsonify({"201 Created": "HTTP/1.1"})


@app.route('/category/<int:id>', methods=['DELETE'])
def delete_category(id: int) -> wrappers.Response:
    Categories.query.get_or_404(id)
    Categories.delete_note(id)
    return jsonify({"200 OK": "HTTP/1.1"})


@app.route('/category/<int:id>', methods=['PUT'])
def edit_category(id: int) -> wrappers.Response:
    Categories.query.get_or_404(id)
    category = request.form['data']
    if Categories.edit(category, id):
        return jsonify({"403 Forbidden": "HTTP/1.1"})
    return jsonify({"200 OK": "HTTP/1.1"})
