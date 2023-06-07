import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

username = "ashleendaly"
token = os.getenv("ACCESS_TOKEN")
organisation = "JARP-Inc"

all_repositories = requests.get(url="https://api.github.com/orgs/{org}/repos".format(org=organisation), auth=(username, token)).json()

for repo in all_repositories:
    label_added = requests.post(url="https://api.github.com/repos/{owner}/{repo}/labels".format(owner=repo["owner"]["login"],repo=repo["name"]), auth=(username, token), data=json.dumps({
        "name": "in progress",
        "color": "f29513",
        "description": "This issue is currently being worked on"
    })).json()

    # label_deleted = requests.delete(url="https://api.github.com/repos/{owner}/{repo}/labels/{name}".format(owner=repo["owner"]["login"],repo=repo["name"], name="in progress"), auth=(username, token))

    print("Added label to {repo}".format(repo=repo["name"]))
    
