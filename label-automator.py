import requests
from dotenv import load_dotenv
import os

load_dotenv()

username = "ashleendaly"
token = os.getenv("ACCESS_TOKEN")
organisation = "JARP-Inc"

label = {
        "name": "urgent",
        "color": "D22B2B",
        "description": "This issue needs to be resolved immediately."
    }

def get_repositories(organisation, username, token):
    return requests.get(url=f"https://api.github.com/orgs/{organisation}/repos", auth=(username, token)).json()

def add_label_to_repo(repo):
    label_added = requests.post(url=f"https://api.github.com/repos/{repo['owner']['login']}/{repo['name']}/labels", auth=(username, token), data=label).json()
    print(f"Added label to {repo['name']}")
    return label_added

if __name__ == "__main__":
    all_repositories = get_repositories()
    for repo in all_repositories:
        add_label_to_repo(repo)
        
        # label_deleted = requests.delete(url="https://api.github.com/repos/{owner}/{repo}/labels/{name}".format(owner=repo["owner"]["login"],repo=repo["name"], name="in progress"), auth=(username, token))