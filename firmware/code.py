import libs.tasks
import libs.bluetooth
import time
import libs.ui

task_manager = libs.tasks.TaskManager()
ble_manager = libs.bluetooth.BLEManager()

# On startup, load tasks from PC if available
# On sync, overwrite tasks with incoming ones
def clue_main():
    libs.ui.show_ui(libs.ui.setup_ui())

if __name__ == "__main__":
    clue_main()