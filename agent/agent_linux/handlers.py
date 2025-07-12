import subprocess
import random
import time
from urllib.parse import urlparse, parse_qs, unquote
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import tempfile
import datetime
import glob


def safe_run(cmd, shell=False):
    try:
        print(f"[LOG] Запуск команды: {cmd}")
        result = subprocess.run(cmd, shell=shell, check=True)
        print(f"[LOG] Команда завершилась с кодом: {result.returncode}")
    except Exception as e:
        print(f"[ERROR] Ошибка при выполнении команды {cmd}: {e}")

def get_work_dir():
    work_dir = os.path.expanduser("~/LISA_work_files")
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
    return work_dir

def cleanup_old_files():
    work_dir = get_work_dir()
    today = datetime.date.today()
    
    for file_path in glob.glob(os.path.join(work_dir, "*")):
        if os.path.isfile(file_path):
            file_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
            if file_time.date() < today:
                try:
                    os.remove(file_path)
                    print(f"[LOG] Удален старый файл: {file_path}")
                except Exception as e:
                    print(f"[ERROR] Не удалось удалить файл {file_path}: {e}")


# working with apps logic


def handle_firefox(action_data):
    if webdriver is None:
        print("[ERROR] selenium не установлен!")
        return
    

    url = action_data.get("url", "duckduckgo.com")
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    role = action_data.get("role", "user")
    if role == "dev":
        searches = [
            "python programming",
            "linux automation", 
            "selenium webdriver",
            "fastapi tutorial",
            "docker containers"
        ]
    elif role == "admin":
        searches = [
            "linux disk usage",
            "systemctl usage",
            "journalctl logs",
            "linux process monitoring",
            "linux memory usage"
        ]
    else:  # user
        searches = [
            "latest news",
            "weather forecast",
            "easy recipes",
            "new movies",
            "online shopping"
        ]
    
    search_query = random.choice(searches)
    firefox_search_on_url(url, search_query)

def handle_libreoffice_calc(action_data):
    try:
        work_dir = get_work_dir()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"calc_data_{timestamp}.csv"
        file_path = os.path.join(work_dir, filename)
        
        rows = random.randint(5, 15)
        cols = random.randint(3, 8)
        
        headers = [f"Колонка_{i+1}" for i in range(cols)]
        
        with open(file_path, 'w') as f:
            f.write(",".join(headers) + "\n")
            
            for row in range(rows):
                data = [str(random.randint(1, 1000)) for _ in range(cols)]
                f.write(",".join(data) + "\n")
        
        cmd = ["libreoffice", "--calc", file_path]
        print(f"[LOG] Открываем LibreOffice Calc с файлом: {file_path}")
        
        process = subprocess.Popen(cmd)
        time.sleep(random.randrange(5, 15))
        

        try:
            process.terminate()
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            print("[LOG] LibreOffice Calc не закрылся корректно, принудительно завершаем")
            process.kill()
            process.wait()
        
        print(f"[LOG] LibreOffice Calc закрыт, файл сохранен: {file_path}")
        
    except Exception as e:
        print(f"[ERROR] Ошибка при работе с LibreOffice Calc: {e}")

def handle_libreoffice_writer(action_data):
    try:
        work_dir = get_work_dir()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"writer_doc_{timestamp}.txt"
        file_path = os.path.join(work_dir, filename)
        
        paragraphs = random.randint(2, 5)
        sentences = [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Praesent nec bibendum arcu.",
            "Etiam vehicula libero est, ut ultricies mauris vehicula non.",
            "Fusce in congue nunc.",
            "Donec ac efficitur diam.",
            "Ut quis consequat urna, et congue tellus.",
            "Duis pulvinar nisi quis felis ultrices ullamcorper.",
            "Nunc vestibulum euismod nibh, a fringilla tellus mattis non."
        ]
        
        with open(file_path, 'w') as f:
            for _ in range(paragraphs):
                paragraph = " ".join(random.sample(sentences, random.randint(3, 6)))
                f.write(paragraph + "\n\n")
        
        cmd = ["libreoffice", "--writer", file_path]
        print(f"[LOG] Открываем LibreOffice Writer с файлом: {file_path}")
        
        process = subprocess.Popen(cmd)
        time.sleep(random.randrange(5, 15))
        

        try:
            process.terminate()
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            print("[LOG] LibreOffice Writer не закрылся корректно, принудительно завершаем")
            process.kill()
            process.wait()
        
        print(f"[LOG] LibreOffice Writer закрыт, файл сохранен: {file_path}")
        
    except Exception as e:
        print(f"[ERROR] Ошибка при работе с LibreOffice Writer: {e}")

def handle_terminal_command(action_data):
    command = action_data.get("name", "")
    if command:
        safe_run(command.split(), shell=True)
    else:
        print("[WARNING] Пустая команда")

def handle_gimp(action_data):
    try:
        work_dir = get_work_dir()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gimp_image_{timestamp}.png"
        file_path = os.path.join(work_dir, filename)
        
        try:
            cmd = ["convert", "-size", "800x600", "xc:white", file_path]
            safe_run(cmd)
        except:
            with open(file_path, 'w') as f:
                f.write("GIMP placeholder file")
        
        cmd = ["gimp", file_path]
        print(f"[LOG] Открываем GIMP с файлом: {file_path}")
        
        process = subprocess.Popen(cmd)
        time.sleep(random.randrange(5, 15))
        
        try:
            process.terminate()
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            print("[LOG] GIMP не закрылся корректно, принудительно завершаем")
            process.kill()
            process.wait()
        
        print(f"[LOG] GIMP закрыт, файл сохранен: {file_path}")
        
    except Exception as e:
        print(f"[ERROR] Ошибка при работе с GIMP: {e}")

def handle_text_editor(action_data):
    try:
        work_dir = get_work_dir()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"text_doc_{timestamp}.txt"
        file_path = os.path.join(work_dir, filename)
        
        content = [
            "Это автоматически созданный текстовый документ.",
            "Создан: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "",
            "Содержимое документа:",
            "- Строка 1: Информация о проекте",
            "- Строка 2: Заметки и идеи", 
            "- Строка 3: Планы на будущее",
            "",
            "Конец документа."
        ]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
        
        editors = ["gedit", "nano", "vim"]
        editor = None
        
        for ed in editors:
            try:
                result = subprocess.run(["which", ed], capture_output=True, text=True)
                if result.returncode == 0:
                    editor = ed
                    break
            except:
                continue
        
        if not editor:
            print("[WARNING] Не найден подходящий текстовый редактор")
            return
        
        cmd = [editor, file_path]
        print(f"[LOG] Открываем {editor} с файлом: {file_path}")
        
        process = subprocess.Popen(cmd)
        time.sleep(random.randrange(5, 15))
        
        try:
            process.terminate()
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            print(f"[LOG] {editor} не закрылся корректно, принудительно завершаем")
            process.kill()
            process.wait()
        
        print(f"[LOG] {editor} закрыт, файл сохранен: {file_path}")
        
    except Exception as e:
        print(f"[ERROR] Ошибка при работе с текстовым редактором: {e}")

#ACTIVITY CENTER  

def execute_activity_action(activity_name, action_data=None):
    """
    Централизованный диспетчер активностей на основе switch case
    
    Args:
        activity_name (str): Имя активности/команды
        action_data (dict): Дополнительные данные действия (URL, роль и т.д.)
    """
    if action_data is None:
        action_data = {}

    activity_lower = activity_name.lower()

    if "firefox" in activity_lower:
        handle_firefox(action_data)
    elif "libreoffice calc" in activity_lower or "calc" in activity_lower:
        handle_libreoffice_calc(action_data)
    elif "libreoffice writer" in activity_lower or "writer" in activity_lower:
        handle_libreoffice_writer(action_data)
    elif "gimp" in activity_lower:
        handle_gimp(action_data)
    elif "text editor" in activity_lower or "editor" in activity_lower or "nano" in activity_lower or "vim" in activity_lower or "gedit" in activity_lower:
        handle_text_editor(action_data)
    elif "terminal" in activity_lower or "command" in activity_lower:
        handle_terminal_command(action_data)
    else:
        print(f"[WARNING] Неизвестная активность: {activity_name}, пытаемся выполнить как команду")
        handle_terminal_command({"name": activity_name})

#Utilities

def firefox_search_on_url(url, query):
    """Вспомогательная функция для поиска в Firefox"""
    if webdriver is None:
        print("[ERROR] selenium не установлен!")
        return
    driver = None
    try:
        options = Options()
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
    finally:
        if driver is not None:
            driver.quit()

def end_of_day_cleanup():
    cleanup_old_files()

#role handlers

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
        
        if actions and random.random() < 0.7:
            action = random.choice(actions)
            return self._action_to_callable(action, "dev")
        else:
            return random.choice(dev_commands)

    def _action_to_callable(self, action, role):
        if "name" in action and action["name"]:
            action_data = {
                "name": action["name"],
                "url": action.get("url"),
                "role": role
            }
            
            return {
                "name": f"execute {action['name']}",
                "run": lambda: execute_activity_action(action["name"], action_data)
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
        
        if actions and random.random() < 0.6:
            action = random.choice(actions)
            return self._action_to_callable(action, "admin")
        else:
            return random.choice(admin_commands)

    def _action_to_callable(self, action, role):
        if "name" in action and action["name"]:
            action_data = {
                "name": action["name"],
                "url": action.get("url"),
                "role": role
            }
            
            return {
                "name": f"execute {action['name']}",
                "run": lambda: execute_activity_action(action["name"], action_data)
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
        return self._action_to_callable(action, "user")

    def _action_to_callable(self, action, role):
        if "name" in action and action["name"]:
            action_data = {
                "name": action["name"],
                "url": action.get("url"),
                "role": role
            }
            
            return {
                "name": f"execute {action['name']}",
                "run": lambda: execute_activity_action(action["name"], action_data)
            }
        else:
            return {"name": "unknown", "run": lambda: print("Неизвестное действие")}

def emulate_web_action(url, button_id):
    driver = None
    try:
        driver = webdriver.Firefox()
        driver.get(url)
        time.sleep(random.randrange(1,5))
        button = driver.find_element(By.ID, button_id)
        button.click()
        time.sleep(random.randrange(1,5))
    finally:
        if driver is not None:
            driver.quit()
        
