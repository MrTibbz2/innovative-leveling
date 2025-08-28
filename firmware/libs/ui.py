import board, displayio, terminalio, digitalio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
import time
global display
display = board.DISPLAY

def setup_ui() -> displayio.Group:
    main_group = displayio.Group()
    title = label.Label(terminalio.FONT, text="Tasks", color=0xFFFFFF, x=10, y=10, scale=2)
    main_group.append(title)
    # BLE indicator
    ble_indicator = displayio.Group(x=239-55, y=0)
    ble_rect = Rect(x=229, y=0, width=20, height=20, fill=0xFF0000)  # Red by default
    ble_indicator.append(ble_rect)
    ble_label = label.Label(terminalio.FONT, text="BLE status:", color=0xFFFFFF, x=0, y=10, scale=1)
    ble_indicator.append(ble_label)
    main_group.append(ble_indicator)
    # Task area
    task_group = displayio.Group()
    

                         


    return main_group

def show_ui(main_group):
    display.root_group = main_group
    while True:
        time.sleep(1)

