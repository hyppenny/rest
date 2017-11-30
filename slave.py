import requests, json

request = requests.get("http://localhost:5000/hello")
print(json.loads(request.text))
r = requests.post("http://localhost:5000/hello", json={'post': "Hello Master"})
