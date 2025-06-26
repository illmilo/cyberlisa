import subprocess
import random
import aiohttp
import asyncio

class DevHandler:
    async def work(self, params):
        actions = [
            lambda : subprocess.run("git add .", shell=True),
            lambda : subprocess.run("git commit -m 'commit'", shell=True),
            lambda : subprocess.run("git push", shell=True),
            lambda : subprocess.run(["python", random.choice(params["scripts"])])
        ]
        action = random.choice(actions)
        subprocess.run(action, shell=True)
    async def web_surf(self, params):
        async with aiohttp.ClientSession() as session:
            for url in random.sample(params["urls"], 3):
                await session.get(url)
                await asyncio.sleep(random.uniform(1, 3))

class AdminHandler:
    async def work(self,params):
        commands = [
            ["df", "-h"],
            ["free", "-h"],
            ["top", "-bn1"],
            ["systemctl", "status", random.choice(params["services"])]
        ]
        subprocess.run(random.choice(commands), shell=True)

class UserHandler:
    async def work(self, params):
        docs = random.sample(params["docs"], 2)
        subprocess.run("libreoffice", "--writer", docs[0])
        subprocess.run("libreoffice", "--calc", docs[1])
        
