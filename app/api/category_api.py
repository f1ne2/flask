from app import app
from flask import jsonify, wrappers
from app.models import Categories


@app.route('/all_categories')
def all_categories() -> wrappers.Response:
    if Categories().get_all_table():
        return jsonify(dict(Categories().get_all_table()))
    return jsonify({"404": "Not Found"})


@app.route('/category/<int:id>')
def get_category(id: int) -> wrappers.Response:
    category = Categories.query.get_or_404(id)
    return jsonify(category.to_json())


@app.route('/put/<string:category>/<int:id>')
def put_new_category(category: str, id: int) -> wrappers.Response:
    if Categories().check_exist_category(id, category):
        return jsonify({"403 Forbidden": "HTTP/1.1"})
    Categories().put_category(id, category)
    return jsonify({"201 Created": "HTTP/1.1"})


@app.route('/delete/<int:id>')
def delete_category(id: int) -> wrappers.Response:
    Categories.query.get_or_404(id)
    Categories().delete_note(id)
    return jsonify({"200 OK": "HTTP/1.1"})
