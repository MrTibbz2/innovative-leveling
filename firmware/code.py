import libs.bluetooth

import libs.ui
from adafruit_clue import clue

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



def clue_main(): # update loop, ALMOST as slow as turtle but not quite.

    last_highlight = libs.ui.get_highlighted()
    libs.ui.show_ui(libs.ui.setup_ui())
    while True:
        jason = ble_manager.receive_json()
        if jason is not None:
            print("Received JSON:", jason)
            
        if ble_manager.check_reconnect(): libs.ui.show_ui(libs.ui.setup_ui()) 
        prev_highlight = libs.ui.get_highlighted()
        check_and_switch_highlighted()
        current_highlight = libs.ui.get_highlighted()
        if current_highlight != prev_highlight:
            print(f"Highlight changed to {current_highlight}, redrawing UI")
            libs.ui.show_ui(libs.ui.setup_ui()) 
            # man i didnt know you could make a slower graphics library than turtle. 
            # but to be fair, this has no hardware acceleration so.. and it ran out of memory ages ago.
            # i personally think they should make the Applied computing class write their own graphics library
            # every year for the game project, make everyone use last years shit graphics library

                                        



if __name__ == "__main__":
    clue_main() # hi mr o'reagan!

