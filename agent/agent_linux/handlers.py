import subprocess
import random
import aiohttp
import asyncio

class DevHandler:
    async def work(self):
        actions = [
            {"name": "git add", "run": lambda: subprocess.run("git add .", shell=True)},
            {"name": "git commit", "run": lambda: subprocess.run("git commit -m 'commit'", shell=True)},
            {"name": "git push", "run": lambda: subprocess.run("git push", shell=True)},
          #  lambda : subprocess.run(["python", random.choice(params["scripts"])])
        ]
        return random.choice(actions)
    # async def web_surf(self, params):
    #     async with aiohttp.ClientSession() as session:
    #         for url in random.sample(params["urls"], 3):
    #             await session.get(url)
    #             await asyncio.sleep(random.uniform(1, 3))

class AdminHandler:
    async def work(self):
        actions = [
            {"name": "df -h", "run": lambda: subprocess.run(["df", "-h"])},
            {"name": "free -h", "run": lambda: subprocess.run(["free", "-h"])},
            {"name": "top -bn1", "run": lambda: subprocess.run(["top", "-bn1"])},
            #["systemctl", "status", random.choice(params["services"])]
        ]
        return random.choice(actions)

# class UserHandler:
#     async def work(self, params):
#         docs = random.sample(params["docs"], 2)
#         actions = [
#             {"name": "writer", "run": lambda: subprocess.run(["libreoffice", "--writer", docs[0]])},
#             {"name": "calc", "run": lambda: subprocess.run(["libreoffice", "--calc", docs[1]])}
#         ]
#         return random.choice(actions)
        
