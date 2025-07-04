import subprocess
import random
import time
from urllib.parse import urlparse, parse_qs, unquote

def safe_run(cmd, shell=False):
    try:
        print(f"[LOG] Запуск команды: {cmd}")
        result = subprocess.run(cmd, shell=shell, check=True)
        print(f"[LOG] Команда завершилась с кодом: {result.returncode}")
    except Exception as e:
        print(f"[ERROR] Ошибка при выполнении команды {cmd}: {e}")

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
except ImportError:
    webdriver = None
    By = None
    Keys = None

def firefox_search_on_url(url, query):
    if webdriver is None:
        print("[ERROR] selenium не установлен!")
        return
    try:
        options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')  # Отключите для отладки
        driver = webdriver.Firefox(options=options)
        driver.get(url)
        time.sleep(2)
        if "duckduckgo" in url:
            search_box = driver.find_element(By.NAME, "q")
        elif "yandex" in url:
            search_box = driver.find_element(By.NAME, "text")
        else:
            print("[ERROR] Неизвестный сайт для поиска, не могу найти поисковую строку.")
            driver.quit()
            return
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        print(f"[LOG] Выполнен поиск на {url}: {query}")
        time.sleep(random.randrange(10, 20))

        # Найти только настоящие сайты
        if "duckduckgo" in url:
            links = driver.find_elements(By.CSS_SELECTOR, "a.eVNpHGjtxRBq_gLOfGDr")
        elif "yandex" in url:
            links = driver.find_elements(By.CSS_SELECTOR, "a.Link_theme_normal")
        else:
            links = []

        visible_links = [l for l in links if l.is_displayed()]
        if visible_links:
            chosen = random.choice(visible_links)
            href = chosen.get_attribute('href')
            print(f"[LOG] Переход по ссылке: {href}")
            driver.get(href)
            time.sleep(random.randrange(10, 20))
        else:
            print("[LOG] Нет видимых ссылок для перехода.")

        driver.quit()
    except Exception as e:
        print(f"[ERROR] Ошибка при поиске в Firefox: {e}")
        driver.quit()

class DevHandler:
    def work(self, params):
        actions = params.get("actions", [])
        dev_commands = [
            {"name": "git status", "run": lambda: safe_run(["git", "status"])},
            {"name": "python version", "run": lambda: safe_run(["python", "--version"])},
            {"name": "ls -la", "run": lambda: safe_run(["ls", "-la"])},
            {"name": "cat py files", "run": lambda: safe_run(["cat", "*.py"], shell=True)},
            {"name": "echo dev", "run": lambda: safe_run(["echo", "Hello, Dev!"])}
        ]
        if actions and random.random() < 0.5:
            action = random.choice(actions)
            return self._action_to_callable(action)
        else:
            return random.choice(dev_commands)

    def _action_to_callable(self, action):
        if "url" in action and action["url"]:
            searches = [
            {"name": "search python subprocess", "search": "python subprocess"},
            {"name": "search linux automation", "search": "linux automation"},
            {"name": "search selenium headless", "search": "selenium headless"},
            {"name": "search docker compose", "search": "docker compose"},
            {"name": "search asyncio vs threading", "search": "asyncio vs threading"},
            ]
            url = action["url"]
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url
            return {
                "name": f"open {url}",
                "run": lambda: firefox_search_on_url(url, random.choice(searches)["search"])
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
        admin_commands = [
            {"name": "ps aux", "run": lambda: safe_run(["ps", "aux"])},
            {"name": "whoami", "run": lambda: safe_run(["whoami"])},
            {"name": "uptime", "run": lambda: safe_run(["uptime"])},
            {"name": "lsblk", "run": lambda: safe_run(["lsblk"])},
            {"name": "df -h", "run": lambda: safe_run(["df", "-h"])},
            {"name": "free -m", "run": lambda: safe_run(["free", "-m"])},
            {"name": "journalctl -n 10", "run": lambda: safe_run(["journalctl", "-n", "10"])}
        ]
        if actions and random.random() < 0.5:
            action = random.choice(actions)
            return self._action_to_callable(action)
        else:
            return random.choice(admin_commands)

    def _action_to_callable(self, action):
        if "url" in action and action["url"]:
            searches = [
            {"name": "search linux disk usage", "search": "linux disk usage"},
            {"name": "search systemctl usage", "search": "systemctl usage"},
            {"name": "search journalctl logs", "search": "journalctl logs"},
            {"name": "search linux process monitoring", "search": "linux process monitoring"},
            {"name": "search linux memory usage", "search": "linux memory usage"},
            ]
            url = action["url"]
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url
            return {
                "name": f"open {url}",
                "run": lambda: firefox_search_on_url(url, random.choice(searches)["search"])
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
            print("[LOG] Нет доступных действий в конфиге!")
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

def emulate_web_action(url, button_id):
    driver = webdriver.Firefox() 
    driver.get(url)
    time.sleep(random.randrange(1,5))
    button = driver.find_element(By.ID, button_id)
    button.click()
    time.sleep(random.randrange(1,5))
    driver.quit()
        
