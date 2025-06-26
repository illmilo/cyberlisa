import yaml
import time
from croniter import croniter
import random

class BehaviourScheduler:
    def __init__(self, config):
        self.config = config
        self.schedule = self.parse_schedule()
        
    def parse_schedule(self):
        with open(f"activity_templates/{self.config['role']}.yaml") as f:
            return yaml.safe_load(f)
    
    def is_active(self):
        now = time.localtime()
        return self.schedule["work_start_time"] <= now.tm_hour < self.schedule["work_end_time"]
    
    def get_next_action(self):
        actions = self.schedule["actions"]
        weights = [a["probability"] for a in actions]
        return random.choices(actions, weights=weights, k=1)[0]