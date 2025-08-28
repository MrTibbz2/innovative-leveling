import board, displayio, terminalio, digitalio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
import time
global display
display = board.DISPLAY
global BLE_ON
BLE_ON = False
def switch_bluetooth_status_indicator(connected: bool):
    BLE_ON = connected
# Highlight constants (simulate enum)
HIGHLIGHT_NONE = -1
HIGHLIGHT_TASK1 = 0
HIGHLIGHT_TASK2 = 1
HIGHLIGHT_ARROW_UP = 2
HIGHLIGHT_ARROW_DOWN = 3

_highlighted = HIGHLIGHT_NONE  # Default: nothing highlighted

def get_highlighted():
    """Return the current highlighted item."""
    return _highlighted

def change_highlighted():
    """Cycle to the next highlighted item in order: nothing, task1, task2, arrow up, arrow down."""
    global _highlighted
    if _highlighted == HIGHLIGHT_NONE:
        _highlighted = HIGHLIGHT_TASK1
    elif _highlighted == HIGHLIGHT_TASK1:
        _highlighted = HIGHLIGHT_TASK2
    elif _highlighted == HIGHLIGHT_TASK2:
        _highlighted = HIGHLIGHT_ARROW_UP
    elif _highlighted == HIGHLIGHT_ARROW_UP:
        _highlighted = HIGHLIGHT_ARROW_DOWN
    elif _highlighted == HIGHLIGHT_ARROW_DOWN:
        _highlighted = HIGHLIGHT_NONE

# Colors for normal and highlighted states
COLOR_TASK_BG = 0x222233  # Darker
COLOR_TASK_HIGHLIGHT = 0x416080  # Light blue
COLOR_ARROW_BG = 0x222233
COLOR_ARROW_HIGHLIGHT = 0xAACCFF
COLOR_OUTLINE = 0x545C5E
COLOR_OUTLINE_HIGHLIGHT = 0xFFFF00  # Bright yellow

# Example usage in your draw function:
# if get_highlighted() == HIGHLIGHT_TASK1:
#     use COLOR_TASK_HIGHLIGHT and COLOR_OUTLINE_HIGHLIGHT for task1
# else:
#     use COLOR_TASK_BG and COLOR_OUTLINE for task1
# ...repeat for other items...

def thick_outline_rect(x, y, width, height, color, thickness=1, fill=None):
    """
    Returns a displayio.Group containing a single Rect for outline (memory efficient).
    Args:
        x, y: Top-left corner
        width, height: Size
        color: Outline color
        thickness: Outline thickness in pixels (ignored, always 1)
        fill: Fill color (None for transparent)
    """
    group = displayio.Group()
    rect = Rect(x, y, width, height, outline=color, fill=fill)
    group.append(rect)
    return group

def draw_arrow(x, y, direction="up", color=0xFFFFFF, size=32):
    """
    Returns a displayio.Group containing a triangle and a rect to form an arrow.
    Args:
        x, y: Top-left corner of arrow
        direction: "up" or "down"
        color: Arrow color
        size: Arrow size (height)
    """
    group = displayio.Group(x=x, y=y)
    import vectorio
    # Arrow shaft always in the center
    shaft_x = size // 2 - 2
    shaft_width = 4
    shaft_height = size - 12
    if direction == "up":
        shaft_y = 8
        shaft = Rect(x=shaft_x, y=shaft_y, width=shaft_width, height=shaft_height, fill=color)
        group.append(shaft)
        # Upward triangle at top
        points = [
            (size // 2, 0),
            (size // 2 - 10, 12),
            (size // 2 + 10, 12)
        ]
    else:
        shaft_y = 0
        shaft = Rect(x=shaft_x, y=shaft_y, width=shaft_width, height=shaft_height, fill=color)
        group.append(shaft)
        # Downward triangle at bottom
        points = [
            (size // 2, size),
            (size // 2 - 10, size - 12),
            (size // 2 + 10, size - 12)
        ]
    triangle = vectorio.Polygon(pixel_shader=displayio.Palette(1), points=points)
    triangle.pixel_shader[0] = color
    group.append(triangle)
    return group

def setup_ui() -> displayio.Group:
    main_group = displayio.Group()
    title = label.Label(terminalio.FONT, text="Tasks", color=0xFFFFFF, x=10, y=15, scale=3)
    main_group.append(title)
    # BLE indicator
    ble_indicator = displayio.Group(x=239-105, y=0)
    ble_color = 0x00FF00 if BLE_ON else 0xFF0000  # Green if connected, red if not
    ble_rect = Rect(x=75, y=0, width=20, height=20, fill=ble_color)
    ble_indicator.append(ble_rect)
    ble_label = label.Label(terminalio.FONT, text="BLE status:", color=0xAAAAAA, x=0, y=10, scale=1)
    ble_indicator.append(ble_label)
    main_group.append(ble_indicator)
    # Task area
    task_group = displayio.Group(x=5, y=40)
    # Task 1
    task_1 = displayio.Group(x=0, y=0)
    if get_highlighted() == HIGHLIGHT_TASK1:
        task_1_outline = Rect(0, 0, 186, 98, outline=COLOR_OUTLINE_HIGHLIGHT, fill=COLOR_TASK_HIGHLIGHT)  # Slightly darker highlight
        task_1.append(task_1_outline)
    else:
        task_1_outline = Rect(0, 0, 186, 98, outline=COLOR_OUTLINE, fill=COLOR_TASK_BG)
        task_1.append(task_1_outline)
    task_group.append(task_1)
    # Task 2
    task_2 = displayio.Group(x=0, y=98)
    if get_highlighted() == HIGHLIGHT_TASK2:
        task_2_outline = Rect(0, 0, 186, 98, outline=COLOR_OUTLINE_HIGHLIGHT, fill=COLOR_TASK_HIGHLIGHT)
        task_2.append(task_2_outline)
    else:
        task_2_outline = Rect(0, 0, 186, 98, outline=COLOR_OUTLINE, fill=COLOR_TASK_BG)
        task_2.append(task_2_outline)
    task_group.append(task_2)
    main_group.append(task_group)
    # Up arrow
    if get_highlighted() == HIGHLIGHT_ARROW_UP:
        up_arrow_group = draw_arrow(x=239-30, y=40, direction="up", color=COLOR_OUTLINE_HIGHLIGHT, size=32)
    else:
        up_arrow_group = draw_arrow(x=239-30, y=40, direction="up", color=COLOR_ARROW_BG, size=32)
    main_group.append(up_arrow_group)
    # Down arrow
    if get_highlighted() == HIGHLIGHT_ARROW_DOWN:
        down_arrow_group = draw_arrow(x=239-30, y=40+98, direction="down", color=COLOR_OUTLINE_HIGHLIGHT, size=32)
    else:
        down_arrow_group = draw_arrow(x=239-30, y=40+98, direction="down", color=COLOR_ARROW_BG, size=32)
    main_group.append(down_arrow_group)
    return main_group

def show_ui(main_group):
    # Clean up previous root_group if needed
    display.root_group = None
    time.sleep(0.01)  # Give time for GC
    display.root_group = main_group



