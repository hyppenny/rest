import requests, json

def run():
    request = requests.get("http://localhost:5000/commit",json={'pull': False})
    jsonData = json.loads(request.text)
    print(jsonData)
    gitUrl = jsonData['repo']
    print(gitUrl)

    r = requests.post("http://localhost:5000/commit", json={'post': "Yes, Master!"})

if __name__ == "__main__":
    run()