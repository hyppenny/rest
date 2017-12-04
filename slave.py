import requests, json, subprocess


def run():
    request = requests.get("http://localhost:5000/url", json={'pull': False})
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
    request = requests.get("http://localhost:5000/url", json={'pull': True})

    r = requests.get("http://localhost:5000/calculate")
    print(r)
    print(json.loads(r.text))
    json_data = json.loads(r.text)
    print(json_data)
    hashsha = json_data['sha']
    print("Received: {}".format(hashsha))
    bashCommand = "cd pulledRepo &" \
                  "git reset --hard {}".format(hashsha)
    process = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    command_output = process.stdout.read().decode()
    print(command_output)

    command_output = subprocess.check_output(["radon", "cc", "-s", "-a", "pulledRepo"]).decode()
    print(command_output)

    request = requests.post("http://localhost:5000/commit", json={'post': "Yes, Master!"})


if __name__ == "__main__":
    run()
