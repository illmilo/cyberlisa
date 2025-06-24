import time
import json
from croniter import croniter
import datetime
import random
import asyncio

#надо сделать чтобы конфиг json брался из бд и сюда передавался

class Behaviour:
    def __init__ (self, config):
        self.config = config
        self.schedule = self.get_schedule()
        self.activity_rate = self.config.get("activity_rate", 1.0)
    
    def get_schedule(self):
        return croniter(self.config["schedule"]).get_next(datetime.datetime.now())
    
    def isActive(self):
        now = datetime.datetime.now()
        return self.schedule["start_time"] <= now < self.schedule["end_time"]
    
    def get_next_action(self):
        actions = self.config["actions"]
        weights = [a["probability"] for a in actions]
        return random.choices(actions, weights=weights)[0]
    
    async def run_loop(self, action_func):
        while True:
            # Чем выше activity_rate, тем выше шанс действия в каждом цикле
            if random.random() < min(self.activity_rate, 1.0):
                action = self.get_next_action()
                print(f"Выполняется действие: {action['name']}")
                # Длительность действия зависит от activity_rate (чем выше, тем короче пауза)
                action_duration = random.uniform(1, 3) / max(self.activity_rate, 0.1)
                if asyncio.iscoroutinefunction(action_func):
                    await action_func(action)
                else:
                    action_func(action)
                await asyncio.sleep(action_duration)
            # Пауза между попытками действий
            pause = random.uniform(1, 5) / max(self.activity_rate, 0.1)
            await asyncio.sleep(pause)
    