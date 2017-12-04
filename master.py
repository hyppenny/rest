from time import sleep, time

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
        self.startTime = 0
        self.repoCCs = []
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


class calculateCC(Resource):
    def get(self):
        self.master = m
        self.reqparser = reqparse.RequestParser()

        self.reqparser.add_argument('commit', type=str, location='json')
        self.reqparser.add_argument('complexity', type=str, location='json')
        if self.master.currSlaveNum < self.master.slaveNum:
            sleep(0.1)
            return {'sha': 1}
        if len(self.master.repoCommits) == 0:
            return {'sha': 0}
        commitSha = self.master.repoCommits[0]
        del self.master.repoCommits[0]
        print(commitSha)
        return {'sha': commitSha}

    def post(self):
        self.master = m
        self.reqparser = reqparse.RequestParser()

        self.reqparser.add_argument('commit', type=str, location='json')
        self.reqparser.add_argument('complexity', type=str, location='json')
        args = self.reqparser.parse_args()
        self.master.repoCCs.append({'sha': args['commit'], 'complexity': args['complexity']})
        if len(self.master.repoCCs) == self.master.repoCommitsCount:
            endTime = time() - self.master.startTime
            totalComplexity = 0
            for x in self.master.repoCCs:
                xcomp = float(x['complexity'])
                if xcomp > 0:
                    totalComplexity += xcomp
                else:
                    print("Commit {} has no computable files".format(x['sha']))
            averageComplexity = totalComplexity / len(self.master.repoCCs)
            print("\n\nAverage cyclomatic complexity for the repository ({}) is: {}".format(self.master.repoAddress,
                                                                                            averageComplexity))
            print("{} slaves finished work in {} seconds\n\n".format(self.master.repoCommitsCount, endTime))
        return {'success': True}


class sendUrl(Resource):
    def get(self):
        self.master = m
        self.req = reqparse.RequestParser()
        self.req.add_argument('pull', type=int, location='json')
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


api.add_resource(calculateCC, '/calculate')
api.add_resource(sendUrl, '/url')

if __name__ == '__main__':
    m = master()
    app.run(port=5000)
