import requests, json, subprocess


def run():
    request = requests.get("http://localhost:6666/url", json={'pull': False})
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
    requests.get("http://localhost:6666/url", json={'pull': True})
    numDone = 0
    nextCommit = True
    while nextCommit:
        r = requests.get("http://localhost:6666/calculate")
        print(r)
        print(json.loads(r.text))
        json_data = json.loads(r.text)
        print(json_data)
        hashsha = json_data['sha']
        print("Received: {}".format(hashsha))
        if hashsha == 1:
            print("Waiting for enough workers...")
        else:
            if hashsha == 0:
                print("No commit left")
                break

            bashCommand = "cd repo &" \
                          "git reset --hard {}".format(hashsha)
            process = subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            command_output = process.stdout.read().decode()
            print(command_output)

            command_output = subprocess.check_output(["radon", "cc", "-s", "-a", "repo"]).decode()
            print(command_output)

            if command_output[command_output.rfind('(') + 1:-2] == "":
                print("NO RELEVENT FILES")
                r = requests.post("http://localhost:6666/calculate",
                                  json={'commit': hashsha, 'complexity': -1})
            else:
                averageCC = float(command_output[command_output.rfind("(") + 1:-2].strip(')'))
                r = requests.post("http://localhost:6666/calculate",
                                  json={'commit': hashsha, 'complexity': averageCC})
            numDone += 1
    print("\n\nCalculated the cyclomatic complexity for {} commits.\n\n".format(numDone))


if __name__ == "__main__":
    run()
