import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

labels = {
        "name": "retrospective",
        "color": "d8278d",
        "description": "This issue is to be discussed in the next retrospective."
    }

def gather_input(item_to_gather):
    gathered_input = input(f"Enter your {item_to_gather}: ")
    if (validate(gathered_input) == True):
        return gathered_input
    else:
        return gather_input(item_to_gather) 

def validate(unconfirmed_input):
    confirmation = input(f"Are you sure {unconfirmed_input} is correct? y/n [y]: ")
    if confirmation == "y" or confirmation == "":
        return True
    elif confirmation == "n":
        print("Please try again.")
        return False
    else:
        print("Invalid input. Please try again.")
        return False

async def get_repositories(organisation, username, token):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.github.com/orgs/{organisation}/repos", auth=(username, token))
    return response.json()

async def add_label_to_repo(repo, username, token):
    async with httpx.AsyncClient() as client:
        response = await client.post(url=f"https://api.github.com/repos/{repo['owner']['login']}/{repo['name']}/labels", auth=(username, token), json=labels)
        print(f"Added label to {repo['name']}")
        return response

async def main():
    username = gather_input("GitHub username")
    token = gather_input("GitHub token")
    organisation = gather_input("GitHub organisation")

    all_repositories = await get_repositories(organisation, username, token)
    tasks = [add_label_to_repo(repo, username, token) for repo in all_repositories]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
