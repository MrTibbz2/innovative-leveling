# 2025 Lachlan McKenna
# UI for displaying all tasks and statuses on the Adafruit Clue

import displayio, terminalio
from board import DISPLAY
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
import gc
# import vectorio
STATUS_NAMES = ("TODO", "IN PROGRESS", "DONE")
global BLE_ON, _ui_group, _task1_status, _task1_name, _task1_due, _task2_status, _task2_name, _task2_due, _ble_rect
BLE_ON = False
_ui_group = None
_task1_status = None
_task1_name = None
_task1_due = None
_task2_status = None
_task2_name = None
_task2_due = None
_ble_rect = None

def switch_bluetooth_status_indicator(connected: bool):
    global BLE_ON, _ble_rect
    BLE_ON = connected
    if _ble_rect:
        _ble_rect.fill = 0x00FF00 if connected else 0xFF0000
# Highlight constants. enums dont exist in circuitpython, but i love enums C++ my goat


# Colors when stuff is selected
COLOR_TASK_BG = 0x222233  
COLOR_TASK_HIGHLIGHT = 0x416080  
COLOR_OUTLINE = 0x545C5E
COLOR_OUTLINE_HIGHLIGHT = 0xFFFF00  # if you wanna know what this colour is, then look at a colour picker dumbass




# def draw_arrow(x: int, y: int, direction="up", color=0xFFFFFF, size=32) -> displayio.Group:
#     """
#     Returns a displayio.Group containing a triangle and a rect to form an arrow.
#     Args:
#         x, y: Top-left corner of arrow
#         direction: "up" or "down"
#         color: Arrow color
#         size: Arrow size (height)
#     """
#     group = displayio.Group(x=x, y=y)

#     # Arrow shaft always in the center
#     shaft_x = size // 2 - 2
#     shaft_width = 4
#     shaft_height = size - 12
#     if direction == "up":
#         shaft_y = 8
#         shaft = Rect(x=shaft_x, y=shaft_y, width=shaft_width, height=shaft_height, fill=color)
#         group.append(shaft)
#         # Upward triangle at top
#         points = [
#             (size // 2, 0),
#             (size // 2 - 10, 12),
#             (size // 2 + 10, 12)
#         ]
#     else:
#         shaft_y = 0
#         shaft = Rect(x=shaft_x, y=shaft_y, width=shaft_width, height=shaft_height, fill=color)
#         group.append(shaft)
#         # Downward triangle at bottom
#         points = [
#             (size // 2, size),
#             (size // 2 - 10, size - 12),
#             (size // 2 + 10, size - 12)
#         ]
#     triangle = vectorio.Polygon(pixel_shader=displayio.Palette(1), points=points)
#     triangle.pixel_shader[0] = color
#     group.append(triangle)
#     return group

def setup_ui(task_manager=None, current_task_index=0) -> displayio.Group:
    global _ui_group, _task1_status, _task1_name, _task1_due, _task2_status, _task2_name, _task2_due, _ble_rect
    
    if _ui_group is None:
        _ui_group = displayio.Group()
        _ui_group.append(label.Label(terminalio.FONT, text="Tasks", color=0xFFFFFF, x=10, y=15, scale=3))
        _ble_rect = Rect(x=209, y=0, width=20, height=20, fill=0xFF0000)
        _ui_group.append(_ble_rect)
        _ui_group.append(label.Label(terminalio.FONT, text="BLE status:", color=0xAAAAAA, x=134, y=10, scale=1))
        _ui_group.append(Rect(5, 40, 186, 98, outline=COLOR_OUTLINE, fill=COLOR_TASK_BG))
        _task1_status = label.Label(terminalio.FONT, text="", color=0xFFFFFF, x=10, y=55, scale=1)
        _task1_name = label.Label(terminalio.FONT, text="", color=0xFFFFFF, x=10, y=75, scale=1)
        _task1_due = label.Label(terminalio.FONT, text="", color=0xAAAAAA, x=10, y=95, scale=1)
        _ui_group.append(_task1_status)
        _ui_group.append(_task1_name)
        _ui_group.append(_task1_due)
        _ui_group.append(Rect(5, 138, 186, 98, outline=COLOR_OUTLINE, fill=COLOR_TASK_BG))
        _task2_status = label.Label(terminalio.FONT, text="", color=0xFFFFFF, x=10, y=153, scale=1)
        _task2_name = label.Label(terminalio.FONT, text="", color=0xFFFFFF, x=10, y=173, scale=1)
        _task2_due = label.Label(terminalio.FONT, text="", color=0xAAAAAA, x=10, y=193, scale=1)
        _ui_group.append(_task2_status)
        _ui_group.append(_task2_name)
        _ui_group.append(_task2_due)
    
    _ble_rect.fill = 0x00FF00 if BLE_ON else 0xFF0000
    
    if task_manager.tasks and current_task_index < len(task_manager.tasks):
        task = task_manager.tasks[current_task_index]
        _task1_status.text = STATUS_NAMES[task.status]
        _task1_name.text = task.name[:20]
        _task1_due.text = f"Due: {task.due or 'None'}"
    else:
        _task1_status.text = ""
        _task1_name.text = ""
        _task1_due.text = ""
    
    if task_manager.tasks and len(task_manager.tasks) > 1:
        next_index = (current_task_index + 1) % len(task_manager.tasks)
        task = task_manager.tasks[next_index]
        _task2_status.text = STATUS_NAMES[task.status]
        _task2_name.text = task.name[:20]
        _task2_due.text = f"Due: {task.due or 'None'}"
    else:
        _task2_status.text = ""
        _task2_name.text = ""
        _task2_due.text = ""
    
    return _ui_group

def show_ui(main_group):
    DISPLAY.root_group = None  # Clear existing content
    gc.collect() 
    DISPLAY.root_group = main_group



