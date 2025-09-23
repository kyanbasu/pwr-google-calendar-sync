import sys
from modules.uiHelper import (
    clear_screen,
    header,
    get_key,
    set_foreground,
    reset_formatting,
    set_background,
)

# Define menu options and their associated colors
menu_options = [
    ("Sync update", "#ffa500"),
    ("Sync without updating", "#ffa500"),
    ("Edit sync config", "#9da0e2"),
    ("Calendar Info", "#a2d3e0"),
    ("Delete", "#ff88aa"),
    ("Exit", "#ff3030"),
]

selected_index = 0


def reset():
    global selected_index
    selected_index = 0


def main():
    global selected_index
    clear_screen()

    header(" PWR google calendar synchronization manager ")

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
            case "Sync update":
                set_foreground("#ffa900")
                print("You selected Run. Executing run sequence...")
                reset_formatting()

            case "Edit sync config":
                from windows.windowManager import change_window, Window

                change_window(Window.config)
                return
            case "Delete":
                pass
            case "Exit":
                sys.exit(0)
            case _:
                print("Option not found")

        input("\nPress Enter to return to the menu...")
