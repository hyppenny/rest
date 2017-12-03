import requests, json

def run():
    request = requests.get("http://localhost:5000/commit")
    print(json.loads(request.text))
    r = requests.post("http://localhost:5000/commit", json={'post': "Yes, Master!"})

if __name__ == "__main__":
    run()