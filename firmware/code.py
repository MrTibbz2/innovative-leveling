import libs.tasks
import libs.bluetooth
import time
import libs.ui
from adafruit_clue import clue
task_manager = libs.tasks.TaskManager()
ble_manager = libs.bluetooth.BLEManager()

_last_a_state = False

def check_and_switch_highlighted():
    """
    Checks if clue.button_a is pressed (edge detection) and switches highlighted item if so.
    Call this in your main loop.
    """
    global _last_a_state
    if clue.button_a and not _last_a_state:
        
        libs.ui.change_highlighted()
        print(f"Button A pressed, switched highlighted to {libs.ui.get_highlighted()}")
    _last_a_state = clue.button_a
# On startup, load tasks from PC if available
# On sync, overwrite tasks with incoming ones
def clue_main():
    last_highlight = libs.ui.get_highlighted()
    libs.ui.show_ui(libs.ui.setup_ui())
    while True:
        prev_highlight = libs.ui.get_highlighted()
        check_and_switch_highlighted()
        current_highlight = libs.ui.get_highlighted()
        if current_highlight != prev_highlight:
            print(f"Highlight changed to {current_highlight}, redrawing UI")
            libs.ui.show_ui(libs.ui.setup_ui())
        time.sleep(0.05)
        


if __name__ == "__main__":
    clue_main()