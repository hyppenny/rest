import requests, json

def run():
    request = requests.get("http://localhost:5000/hello")
    print(json.loads(request.text))
    r = requests.post("http://localhost:5000/hello", json={'post': "Hello Master"})

if __name__ == "__main__":
    run()