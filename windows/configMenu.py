from modules.uiHelper import clear_screen, header, get_key

selected_index = 0


def reset():
    global selected_index
    selected_index = 0


def main():
    from windows.windowManager import change_window, Window

    change_window(Window.main)
