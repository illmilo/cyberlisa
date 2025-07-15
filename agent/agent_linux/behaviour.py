import time
import datetime
import random
from handlers import DevHandler, AdminHandler, UserHandler, end_of_day_cleanup
import requests


def send_heartbeat(employee_id, backend_url="http://localhost:8000"):
    url = f"{backend_url}/agents/{employee_id}/heartbeat"
    try:
        response = requests.post(url, json={"status": "ok"})
        print(f"[HEARTBEAT] Sent heartbeat, status: {response.status_code}")
    except Exception as e:
        print(f"[HEARTBEAT] Failed to send heartbeat: {e}")


class Behaviour:
    def __init__ (self, config):
        self.config = config
        self.activity_rate = self.config.get("activity_rate", 1.0)
        self.handler = self.get_handler()
        self.last_cleanup_date = None
        self.heartbeat_interval = 2 * 60 * 60 
        self.backend_url = "http://localhost:8000"
    
    def isActive(self):
        now = datetime.datetime.now().time()
        start = datetime.time.fromisoformat(self.config["work_start_time"])
        end = datetime.time.fromisoformat(self.config["work_end_time"])
        return start <= now < end
    
    def should_cleanup(self):
        today = datetime.date.today()
        if self.last_cleanup_date != today:
            now = datetime.datetime.now().time()
            start = datetime.time.fromisoformat(self.config["work_start_time"])
            end = datetime.time.fromisoformat(self.config["work_end_time"])
            if start > now >= end: 
                self.last_cleanup_date = today
                return True
        return False
    
    def get_next_action(self):
        return self.handler.work(self.config)
    
    def get_handler(self):
        if self.config["role"] == "dev":
            return DevHandler()
        elif self.config["role"] == "admin":
            return AdminHandler()
        elif self.config["role"] == "user":
            return UserHandler()
        else:
            raise ValueError(f"Unknown role: {self.config['role']}")


    def run_loop(self, action_func=None):
        last_heartbeat = 0
        while True:
            now = time.time()
            if now - last_heartbeat > self.heartbeat_interval:
                send_heartbeat(self.config.get("employee_id", 0), backend_url=self.backend_url)
                last_heartbeat = now
            if self.isActive():
                if self.should_cleanup():
                    print("[LOG] Выполняем очистку файлов в конце рабочего дня")
                    end_of_day_cleanup()
                
                if random.random() < min(self.activity_rate, 1.0):
                    action = self.get_next_action()
                    if action_func:
                        action_func(action)
                    action_duration = random.uniform(1, 3) / max(self.activity_rate, 0.1)
                    action["run"]()
                    time.sleep(action_duration)
                pause = random.uniform(1, 5) / max(self.activity_rate, 0.1)
                time.sleep(pause)
            else:
                time.sleep(60)
    