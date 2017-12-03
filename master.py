from flask import Flask
from flask_restful import Resource, Api, reqparse
import requests,json

app = Flask(__name__)
api = Api(app)


class master():
    def __init__(self):
        request = requests.get("https://api.github.com/repos/flask-restful/flask-restful/commits?page=1&per_page=100")
        print(json.loads(request.text))

class Hello(Resource):
    def get(self):
        return "Hello Slave"

    def post(self):
        r = reqparse.RequestParser()
        r.add_argument('post', type=str, location='json')
        print(r.parse_args()['post'])


api.add_resource(Hello, '/hello')

if __name__ == '__main__':
    m = master()
    app.run(port=5000)
