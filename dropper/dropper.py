import psutil

def find_target_process(process_name):   
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return proc.info['pid']
    return None
if __name__ == "__main__":
    pid = find_target_process("Hyprland")
    print(f"Result: {pid}")
