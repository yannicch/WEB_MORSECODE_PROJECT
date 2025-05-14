from flask_restful import reqparse


parser = reqparse.RequestParser()
parser.add_argument('content', required=True)
parser.add_argument('translation', required=True)
parser.add_argument('created_date', required=True)
parser.add_argument('user_id', required=True, type=int)
