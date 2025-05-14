import flask
from flask import request, jsonify, make_response

from . import db_session
from .trans import Trans

blueprint = flask.Blueprint('trans_api', __name__, template_folder='templates')


@blueprint.route('/api/trans')
def get_trans():
    db_sess = db_session.create_session()
    news = db_sess.query(Trans).all()
    return jsonify(
        {'trans': [item.to_dict(only=('content', 'translation', 'created_date', 'user_id')) for item in news]})


@blueprint.route('/api/trans/<int:trans_id>', methods=['GET'])
def get_one_trans(trans_id):
    db_sess = db_session.create_session()
    trans = db_sess.query(Trans).get(trans_id)
    if not trans:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify({'trans': trans.to_dict(only=('content', 'translation', 'created_date', 'user_id'))})


@blueprint.route('/api/trans/<int:trans_id>', methods=['DELETE'])
def delete_trans(trans_id):
    db_sess = db_session.create_session()
    trans = db_sess.query(Trans).get(trans_id)
    if not trans:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(trans)
    db_sess.commit()
    return jsonify({'success': 'OK'})
