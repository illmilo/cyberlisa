import subprocess
import random
import time

def safe_run(cmd, shell=False):
    try:
        subprocess.run(cmd, shell=shell, check=True)
    except Exception as e:
        print(f"[ERROR] Ошибка при выполнении команды {cmd}: {e}")

class DevHandler:
    def work(self, params):
        actions = params.get("actions", [])
        if not actions:
            print("[LOG] Нет действий в конфиге")
            return {"name": "no_action", "run": lambda: print("Нет действия")}
        action = random.choice(actions)
        return self._action_to_callable(action)

    def _action_to_callable(self, action):
        if "url" in action and action["url"]:
            url = action["url"]
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url
            return {
                "name": f"open {url}",
                "run": lambda: safe_run(["xdg-open", url])
            }
        elif "name" in action and action["name"]:
            return {
                "name": action["name"],
                "run": lambda: safe_run([action["name"]])
            }
        else:
            return {"name": "unknown", "run": lambda: print("Неизвестное действие")}

class AdminHandler:
    def work(self, params):
        actions = params.get("actions", [])
        if not actions:
            print("[LOG] Нет действий в конфиге")
            return {"name": "no_action", "run": lambda: print("Нет действия")}
        action = random.choice(actions)
        return self._action_to_callable(action)

    def _action_to_callable(self, action):
        if "url" in action and action["url"]:
            url = action["url"]
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url
            return {
                "name": f"open {url}",
                "run": lambda: safe_run(["xdg-open", url])
            }
        elif "name" in action and action["name"]:
            return {
                "name": action["name"],
                "run": lambda: safe_run([action["name"]])
            }
        else:
            return {"name": "unknown", "run": lambda: print("Неизвестное действие")}

class UserHandler:
    def work(self, params):
        actions = params.get("actions", [])
        if not actions:
            print("[LOG] Нет действий в конфиге")
            return {"name": "no_action", "run": lambda: print("Нет действия")}
        action = random.choice(actions)
        return self._action_to_callable(action)

    def _action_to_callable(self, action):
        if "url" in action and action["url"]:
            url = action["url"]
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url
            return {
                "name": f"open {url}",
                "run": lambda: safe_run(["xdg-open", url])
            }
        elif "name" in action and action["name"]:
            return {
                "name": action["name"],
                "run": lambda: safe_run([action["name"]])
            }
        else:
            return {"name": "unknown", "run": lambda: print("Неизвестное действие")}
        
