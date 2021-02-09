from __future__ import annotations
from app import db
from app.api.api_interface import Connection
from app.models import Categories, Questions, Answers
from typing import List


class Requests(Connection):
    def put(self, category_id: str, added: str) -> None:
        note = Categories(category_id=category_id, category_name=added)
        db.session.add(note)
        db.session.commit()

    def get(self) -> List[list]:
        result = db.session.query(Categories).all()
        return [[element.category_id, element.category_name] for element in
                result]

    def delete(self, category_id: str) -> None:
        delt = db.session.query(Categories).filter_by\
            (category_id=category_id).one()
        db.session.delete(delt)
        db.session.commit()
