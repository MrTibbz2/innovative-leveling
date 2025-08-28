import board, displayio, terminalio, digitalio
from adafruit_display_text import label
from adafruit_display_shapes.rect import Rect
import time
global display
display = board.DISPLAY

def thick_outline_rect(x, y, width, height, color, thickness=3, fill=None):
    """
    Returns a displayio.Group containing multiple Rects to simulate a thick outline.
    Args:
        x, y: Top-left corner
        width, height: Size
        color: Outline color
        thickness: Outline thickness in pixels
        fill: Fill color (None for transparent)
    """
    group = displayio.Group()
    # Draw outermost to innermost
    for t in range(thickness):
        rect = Rect(
            x + t,
            y + t,
            width - 2 * t,
            height - 2 * t,
            outline=color,
            fill=fill if t == thickness - 1 else None
        )
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
    ble_rect = Rect(x=75, y=0, width=20, height=20, fill=0xFF0000)  # Red by default
    ble_indicator.append(ble_rect)
    ble_label = label.Label(terminalio.FONT, text="BLE status:", color=0xFFFFFF, x=0, y=10, scale=1)
    ble_indicator.append(ble_label)
    main_group.append(ble_indicator)
    # Task area
    task_group = displayio.Group(x=5, y=40)
    # Thick outlined rectangle for task area
    task_outline = thick_outline_rect(x=0, y=0, width=186, height=196, color=0x545C5E, thickness=4)
    task_group.append(task_outline)
    # TODO: add literally anything

    task_1 = displayio.Group(x=0, y=0)
    task_1_outline = thick_outline_rect(x=0, y=0, width=186, height=98, color=0x545C5E, thickness=4, fill=0xBCCBCE)
    task_1.append(task_1_outline)
    task_group.append(task_1)
    task_2 = displayio.Group(x=0, y=98)
    task_2_outline = thick_outline_rect(x=0, y=0, width=186, height=98, color=0x545C5E, thickness=4, fill=0xBCCBCE)
    task_2.append(task_2_outline)
    task_group.append(task_2)
    main_group.append(task_group)

    # Up arrow
    up_arrow_group = draw_arrow(x=239-30, y=40, direction="up", color=0xFFFFFF, size=32)
    main_group.append(up_arrow_group)
    # Down arrow
    down_arrow_group = draw_arrow(x=239-30, y=40+98, direction="down", color=0xFFFFFF, size=32)
    main_group.append(down_arrow_group)

    return main_group

def show_ui(main_group):
    display.root_group = main_group
    while True:
        time.sleep(1)

