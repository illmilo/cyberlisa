import time
import datetime
import random
from handlers import DevHandler, AdminHandler, UserHandler

class Behaviour:
    def __init__ (self, config):
        self.config = config
        self.activity_rate = self.config.get("activity_rate", 1.0)
        self.handler = self.get_handler()
    
    def isActive(self):
        now = datetime.datetime.now().time()
        start = datetime.time.fromisoformat(self.config["work_start_time"])
        end = datetime.time.fromisoformat(self.config["work_end_time"])
        return start <= now < end
    
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
        while True:
            if self.isActive():
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
    