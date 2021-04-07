import unittest
from requests import put, get, post, delete
from flask import jsonify, request, make_response
from test_models import app, MySQLAlchemy, Categories, Questions, Answers
from typing import List


@app.route('/categories/', methods=['GET'])
def categories():
    category = request.form['data']
    return jsonify(dict(Categories.get_categories()))


def get_categories() -> List[list]:
    result = db.session.query(Categories).all()
    return [[element.category_id, element.category_name] for element in
            result]
# put('http://localhost:5000/categories', data={'data': 'Remember the milk'}).json()

# @app.route('/category/<int:id>', methods=['GET'])
# def get_category(id: int) -> wrappers.Response:
#     category = Categories.query.get_or_404(id)
#     return jsonify(category.to_json())
#
#
# @app.route('/category/', methods=['POST'])
# def add_category() -> wrappers.Response:
#     category = request.form['data']
#     if Categories.check_exist_category(category):
#         return jsonify({"403 Forbidden": "HTTP/1.1"})
#     Categories.add(category)
#     return jsonify({"201 Created": "HTTP/1.1"})
#
#
# @app.route('/category/<int:id>', methods=['DELETE'])
# def delete_category(id: int) -> wrappers.Response:
#     Categories.query.get_or_404(id)
#     Categories.delete_note(id)
#     return jsonify({"200 OK": "HTTP/1.1"})
#
#
# @app.route('/category/<int:id>', methods=['POST'])
# def edit_category(id: int) -> wrappers.Response:
#     Categories.query.get_or_404(id)
#     category = request.form['data']
#     if Categories.check_exist_category(category):
#         return jsonify({"403 Forbidden": "HTTP/1.1"})
#     Categories.edit(category)
#     return jsonify({"200 OK": "HTTP/1.1"})


