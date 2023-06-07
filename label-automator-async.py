import asyncio
import httpx
from dotenv import load_dotenv
import csv

load_dotenv()

def import_labels_from_csv(file_name):
    labels = []

    with open(file_name, newline='') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for i, row in enumerate(csv_reader):
            if i == 0:
                continue
            else:
                labels.append({
                    "name": row[0],
                    "description": row[1],
                    "color": row[2]
                })
            
    
    return labels

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

async def add_labels_to_repo(repo, username, token, label):
    async with httpx.AsyncClient() as client:
        response = await client.post(url=f"https://api.github.com/repos/{repo['owner']['login']}/{repo['name']}/labels", auth=(username, token), json=label)
        print(f"Added label to {repo['name']}")
        return response
        

async def main():

    username = gather_input("GitHub username")
    token = gather_input("GitHub token")
    organisation = gather_input("GitHub organisation")
    file_name = gather_input("CSV file name")


    labels = import_labels_from_csv(file_name)

    all_repositories = await get_repositories(organisation, username, token)

    tasks = [add_labels_to_repo(repo, username, token, label) for label in labels for repo in all_repositories]

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
