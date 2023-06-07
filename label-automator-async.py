import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv()

username = "ashleendaly"
token = os.getenv("ACCESS_TOKEN")
organisation = "JARP-Inc"

label = {
        "name": "in progress",
        "color": "f29513",
        "description": "This issue is currently being worked on"
    }

async def get_repositories():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.github.com/orgs/{organisation}/repos", auth=(username, token))
    return response.json()

async def add_label_to_repo(repo):
    async with httpx.AsyncClient() as client:
        response = await client.post(url=f"https://api.github.com/repos/{repo['owner']['login']}/{repo['name']}/labels", auth=(username, token), json=label)
        print(f"Added label to {repo['name']}")
        return response

async def main():
    all_repositories = await get_repositories()

    tasks = [add_label_to_repo(repo) for repo in all_repositories]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
