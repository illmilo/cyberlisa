import sys
import os
import json
from behaviour import Behaviour

    
def get_data_file_path(filename):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, filename)


def agent_worker(config):
    agent = Behaviour(config)
    def action_func(action):
        print(f"Агент выполняет действие: {action['name']}")
    agent.run_loop(action_func)

def main():
    config_path = get_data_file_path('agent_config.json')
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Файл конфига не найден")
        sys.exit(1)
    agent_worker(config)

if __name__ == "__main__":
    main()
