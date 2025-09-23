from enum import Enum
from windows import mainMenu, configMenu


class Window(Enum):
    """
    Defines submenus with their own choices loop
    """

    main = 0
    config = 1


windows = {
    Window.main: mainMenu,
    Window.config: configMenu,
}

selected_window = Window.main


def change_window(new_window):
    global selected_window
    windows[new_window].reset()
    selected_window = new_window


def main_loop():
    windows[selected_window].main()
