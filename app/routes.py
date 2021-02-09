from app import api
from flask import Flask, render_template, request, url_for
from flask_restful import Resource, Api, reqparse
from app.api.api_interface import Connection
from app.repository.db_requests import Requests


class Routes:
    def __init__(self, interface: Connection):
        self.interface = interface

    def add(self, category_id: str, added: str) -> None:
        category_id = category_id.split("_")[1]
        self.interface.put(category_id, added)

    def delete(self, category_id: str) -> None:
        self.interface.delete(category_id)

    def get(self) -> dict:
        return dict(self.interface.get())


all_categories = {}
req = Requests()
data = Routes(req)


class ListCategories(Resource):
    def put(self, category_id) -> dict:
        data.add(category_id, request.form['data'])
        return {category_id: [all_categories[category_id], "201 Created",
                              "HTTP/1.1"]}


class DeleteCategory(Resource):
    def delete(self, id) -> dict:
        data.delete(id)
        return {id: ["200 OK", "HTTP/1.1"]}


class AllCategories(Resource):
    def get(self):
        return {"200 OK HTTP/1.1": data.get()}


api.add_resource(ListCategories, '/<string:category_id>')
api.add_resource(DeleteCategory, '/delete/<int:id>')
api.add_resource(AllCategories, '/all_categories')
