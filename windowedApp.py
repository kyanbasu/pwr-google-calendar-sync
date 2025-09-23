import os
import sys
from enum import Enum
import time

from modules.ui import get_key

# Define menu options and their associated colors
menu_options = [
    ("Sync update", "255;165;0"),
    ("Sync without updating", "255;165;0"),
    ("Edit sync config", "120;140;230"),
    ("Calendar Info", "173;216;230"),
    ("Delete", "255;105;180"),
    ("Exit", "255;40;40"),
]


class Page(Enum):
    """
    Defines submenus with their own choices loop
    """

    main = 0
    config = 1


# Enable ANSI escape codes on Windows
if os.name == "nt":
    from ctypes import windll, byref
    from ctypes.wintypes import DWORD

    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    STD_OUTPUT_HANDLE = -11
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    mode = DWORD()
    windll.kernel32.GetConsoleMode(h, byref(mode))
    mode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
    windll.kernel32.SetConsoleMode(h, mode)


def draw_menu(selected_index):
    """Clear the screen and draw the menu with a highlighted selection."""
    os.system("cls" if os.name == "nt" else "clear")

    # Header with bold and underlined cyan text
    print(
        "\033[1;4m\033[38;2;0;255;255m"
        + " PWR google calendar synchronization manager ".center(50, "=")
    )
    print("\033[0m")
    print()

    for i, (text, color) in enumerate(menu_options):
        # Highlight the currently selected option using inverse video
        if i == selected_index:
            print("\033[7m\033[38;2;" + color + "m" + text.center(50) + "\033[0m")
        else:
            print("\033[38;2;" + color + "m" + text.center(50) + "\033[0m")
    print("=" * 50)


def main():
    selected_index = 0
    currentPage = Page.main

    while True:
        if currentPage != Page.main:
            from windows.config import main as configLoop

            configLoop()
            continue

        draw_menu(selected_index)
        key = None
        # Wait until a relevant key is pressed
        while key is None:
            key = get_key()
        if key == "CTRLC":
            sys.exit(0)

        if key == "UP":
            selected_index = (selected_index - 1) % len(menu_options)
        elif key == "DOWN":
            selected_index = (selected_index + 1) % len(menu_options)
        elif key == "ENTER":
            # Clear the screen and process the selected option
            os.system("cls" if os.name == "nt" else "clear")
            match menu_options[selected_index][0]:
                case "Sync update":
                    print(
                        "\n\033[38;2;255;165;0mYou selected Run. Executing run sequence...\033[0m"
                    )

                case "Edit sync config":
                    currentPage = Page.config
                case "Delete":
                    print(
                        "\n\033[38;2;255;105;180mYou selected Delete. Initiating delete operation...\033[0m"
                    )
                case "Exit":
                    sys.exit(0)
                case _:
                    print("Option not found")

            if currentPage == Page.main:
                input("\nPress Enter to return to the menu...")


if __name__ == "__main__":
    main()
