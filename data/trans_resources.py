from flask import jsonify
from flask_restful import reqparse, abort, Api, Resource
from data import db_session
from data.reqparse import parser
from data.trans import Trans


def abort_if_news_not_found(trans_id):
    session = db_session.create_session()
    news = session.query(Trans).get(trans_id)
    if not news:
        abort(404, message=f" {trans_id} not found, but you can change it")


class TransResource(Resource):
    def get(self, trans_id):
        abort_if_news_not_found(trans_id)
        session = db_session.create_session()
        trans = session.query(Trans).get(trans_id)
        return jsonify({'trans': trans.to_dict(
            only=('content', 'translation', 'created_date', 'user_id'))})

    def delete(self, trans_id):
        abort_if_news_not_found(trans_id)
        session = db_session.create_session()
        trans = session.query(Trans).get(trans_id)
        session.delete(trans)
        session.commit()
        return jsonify({'success': 'OK'})


class TransListResource(Resource):
    def get(self):
        session = db_session.create_session()
        trans = session.query(Trans).all()
        return jsonify({'news': [item.to_dict(
            only=('content', 'translation', 'created_date', 'user_id')) for item in trans]})

