from flask import Flask
from flask_restful import Resource, Api, reqparse
import requests, json

app = Flask(__name__)
api = Api(app)


class master():
    def __init__(self):
        self.repoCommits = []
        self.repoCommitsCount = 0
        self.slaveNum = int(input("Number of slave needed:"))
        self.currSlaveNum = 0
        self.repoAddress = input("\nRepository address as formate(user/repostory)\n"
                                 "Press enter use default(python/core-workflow)\n"
                                 "Input the repository you want to calculate:")
        if len(self.repoAddress) == 0:
            self.repoAddress = "python/core-workflow"

        self.getCommit(self.repoAddress)

    def getCommit(self, repoAddress):
        githubData = []
        page = 1
        end = False
        while not end:
            request = requests.get(
                "https://api.github.com/repos/{}/commits?page={}&per_page=100".format(repoAddress, page))
            githubData += json.loads(request.text)
            if len(githubData) < page * 100:
                end = True
            page += 1
        for g in githubData:
            self.repoCommits.append(g['sha'])
            print(g['sha'])
            self.repoCommitsCount += 1

        print("\n\n", self.repoCommitsCount)


class Hello(Resource):
    def get(self):
        return "Hello Slave"

    def post(self):
        r = reqparse.RequestParser()
        r.add_argument('post', type=str, location='json')
        print(r.parse_args()['post'])


class distributeCommit(Resource):
    def get(self):
        self.master = m
        self.req = reqparse.RequestParser()
        self.req.add_argument('pull',type=int, location='json')
        args = self.req.parse_args()
        if args['pull'] == False:
            print("!!")
            return {'repo': "https://github.com/{}".format(self.master.repoAddress)}
        if args['pull'] == True:
            self.master.currSlaveNum += 1
            print("Current slave number: {}".format(self.master.currSlaveNum))

    def post(self):
        r = reqparse.RequestParser()
        r.add_argument('post', type=str, location='json')
        print(r.parse_args()['post'])


api.add_resource(Hello, '/hello')
api.add_resource(distributeCommit, '/commit')

if __name__ == '__main__':
    m = master()
    app.run(port=5000)
