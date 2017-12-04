import requests, json, subprocess


def run():
    request = requests.get("http://localhost:5000/commit", json={'pull': False})
    jsonData = json.loads(request.text)
    gitUrl = jsonData['repo']
    print(gitUrl)

    bashCommand = "cd repo &" \
                  "rm -rf .git/ &" \
                  "git init &" \
                  "git remote add origin {} &" \
                  "git pull".format(gitUrl)

    process = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = process.stdout.read().decode()
    print(output)

    print("Repository pulled completed")
    r = requests.get("http://localhost:5000/commit", json={'pull': True})

    r = requests.post("http://localhost:5000/commit", json={'post': "Yes, Master!"})


if __name__ == "__main__":
    run()
