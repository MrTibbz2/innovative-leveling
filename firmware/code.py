# 2025 Lachlan McKenna
# main clue entry point

import libs.bluetooth
import libs.ui
import libs.taskManager
from adafruit_clue import clue
import gc
ble_manager = libs.bluetooth.BLEManager()
task_manager = libs.taskManager.taskManager()

_last_a_state = False
_last_b_state = False
_current_task_index = 0
_last_checksum = ""

# def checksum_dict(obj):
#     """Compute a simple checksum of nested dicts/lists without building JSON."""
#     checksum = 0
#     if isinstance(obj, dict):
#         for key in sorted(obj.keys()):
#             checksum = (checksum + checksum_dict(key)) % 65535
#             checksum = (checksum + checksum_dict(obj[key])) % 65535
#     elif isinstance(obj, list):
#         for item in obj:
#             checksum = (checksum + checksum_dict(item)) % 65535
#     elif isinstance(obj, (int, float, bool)):
#         checksum = (checksum + checksum_dict(str(obj))) % 65535
#     elif obj is None:
#         checksum = (checksum + ord("N")) % 65535
#     else:  # strings
#         for c in str(obj):
#             checksum = (checksum + ord(c)) % 65535
#     return checksum
# libs.taskManager.save_json_to_nvm({"yay": "hi"})

def calculate_tasks_checksum():
    checksum = len(task_manager.tasks)
    for task in task_manager.tasks:
        checksum += task.status
    return checksum

def check_buttons():
    global _last_a_state, _last_b_state, _current_task_index
    
    if clue.button_a and not _last_a_state:
        if task_manager.tasks:
            _current_task_index = (_current_task_index + 1) % len(task_manager.tasks)
            print(f"Scr: {_current_task_index}")
            return True
    _last_a_state = clue.button_a
    
    if clue.button_b and not _last_b_state:
        if task_manager.tasks and _current_task_index < len(task_manager.tasks):
            task = task_manager.tasks[_current_task_index]
            task.status = (task.status + 1) % 3
            print(f"{task.name} st: {task.status}")
            return True
    _last_b_state = clue.button_b
    
    return False



def clue_main():
    global _last_checksum
    
    task_manager.loadTasksFromSave()
    _last_checksum = calculate_tasks_checksum()
    
    libs.ui.show_ui(libs.ui.setup_ui(task_manager, _current_task_index))
    commands = libs.bluetooth.Commands(task_manager, ble_manager)
    while True:
        gc.collect()
        commands.check_commands()
        gc.collect() 
        ui_changed = False
        if ble_manager.check_reconnect():
            ui_changed = True
        
        if check_buttons():
            ui_changed = True
        
        current_checksum = calculate_tasks_checksum()
        if current_checksum != _last_checksum:
            task_manager.dumpTasksToSave()
            _last_checksum = current_checksum
            ui_changed = True
        
        if ui_changed:
            gc.collect()
            libs.ui.show_ui(libs.ui.setup_ui(task_manager, _current_task_index))

                                        



if __name__ == "__main__":
    clue_main() # hi mr o'reagan!

