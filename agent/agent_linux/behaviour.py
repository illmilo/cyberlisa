import time
import json
from croniter import croniter
import datetime
import random

#надо сделать чтобы конфиг json брался из бд и сюда передавался

class Behaviour:
    def __init__ (self, config):
        self.config = config
        self.schedule = self.get_schedule()
    
    def get_schedule(self):
        return croniter(self.config["schedule"]).get_next(datetime.datetime.now())
    
    def isActive(self):
        now = datetime.datetime.now()
        return self.schedule["start_time"] <= now < self.schedule["end_time"]
    
    def get_next_action(self):
        actions = self.config["actions"]
        weights = [a["probability"] for a in actions]
        return random.choices(actions, weights=weights)[0]
    