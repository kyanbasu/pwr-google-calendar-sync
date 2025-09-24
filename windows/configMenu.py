import sys
from turtle import clear
from modules.uiHelper import (
    clear_screen,
    header,
    get_key,
    set_foreground,
    reset_formatting,
    set_background,
)

import yaml

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

COLORS = config["colors"]

# Define menu options and their associated colors
menu_options = [
    ("ICAL URL", "#9da0e2"),
    ("filename", "#9da0e2"),
    ("calendarId", "#9da0e2"),
    ("colors", "#9da0e2"),
    ("Back", "#ff3030"),
]

selected_index = 0


def reset():
    global selected_index
    selected_index = 0


def main():
    global selected_index
    clear_screen()

    header(" Config editor ")

    for i, (text, color) in enumerate(menu_options):
        if i == selected_index:
            set_background(color)
            set_foreground("#000000")
            print(text.center(50))
            reset_formatting()
        else:
            set_foreground(color)
            print(text.center(50))
            reset_formatting()

    header("")

    key = None
    # Wait until a relevant key is pressed
    while key is None:
        key = get_key()

    if key == "UP":
        selected_index = (selected_index - 1) % len(menu_options)
    elif key == "DOWN":
        selected_index = (selected_index + 1) % len(menu_options)
    elif key == "ENTER":
        # Clear the screen and process the selected option
        clear_screen()
        match menu_options[selected_index][0]:
            case "ICAL URL":
                set_foreground("#ffa900")
                print("editing ical")
                reset_formatting()
                input("\nPress Enter to return to the menu...")

            case "colors":
                selected_index2 = 0
                while True:
                    clear_screen()
                    header(" Current colors ")

                    for i, (text, color) in enumerate(COLORS.items()):
                        if i == selected_index2:
                            set_background("#aaaaaa")
                            set_foreground("#000000")
                            print(text.center(50))
                            reset_formatting()
                        else:
                            set_foreground("333")
                            print(text.center(50))
                            reset_formatting()

                    header("")

                    key = None
                    while key is None:
                        key = get_key()

                    if key == "UP":
                        selected_index2 = (selected_index2 - 1) % len(COLORS)
                    elif key == "DOWN":
                        selected_index2 = (selected_index2 + 1) % len(COLORS)
                    elif key == "ENTER":
                        pass

            case "Back":
                from windows.windowManager import change_window, Window

                change_window(Window.main)
                return
            case _:
                print("Option not found")
                input("\nPress Enter to return to the menu...")
