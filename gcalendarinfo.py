from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from modules.gauth import auth

CALENDAR_COLOR_NAMES = {
    '1': 'Cocoa',
    '2': 'Flamingo',
    '3': 'Tomato',
    '4': 'Tangerine',
    '5': 'Pumpkin',
    '6': 'Mango',
    '7': 'Eucalyptus',
    '8': 'Basil',
    '9': 'Pistachio',
    '10': 'Avocado',
    '11': 'Citron',
    '12': 'Banana',
    '13': 'Sage',
    '14': 'Peacock',
    '15': 'Cobalt',
    '16': 'Blueberry',
    '17': 'Lavender',
    '18': 'Wisteria',
    '19': 'Graphite',
    '20': 'Birch',
    '21': 'Radicchio',
    '22': 'Cherry Blossom',
    '23': 'Grape',
    '24': 'Amethyst'
}

EVENT_COLOR_NAMES = {
    '1': 'Lavender',
    '2': 'Sage',
    '3': 'Grape',
    '4': 'Flamingo',
    '5': 'Banana',
    '6': 'Tangerine',
    '7': 'Peacock',
    '8': 'Graphite',
    '9': 'Blueberry',
    '10': 'Basil',
    '11': 'Tomato'
}

SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Ensure command line uses colors
import os
if os.name == 'nt':
    from ctypes import windll, byref
    from ctypes.wintypes import HANDLE, DWORD

    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    STD_OUTPUT_HANDLE = -11

    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    mode = DWORD()
    windll.kernel32.GetConsoleMode(h, byref(mode))
    mode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
    windll.kernel32.SetConsoleMode(h, mode)

def print_color_square(hex_color, amount=1):
    """Print a colored square using ANSI escape codes"""
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    for _ in range(amount):
        print(f"\x1b[48;2;{r};{g};{b}m  \x1b[0m", end="")

if __name__ == "__main__":
    # using gcalendar api
    creds = auth(SCOPES)

    try:
        service = build("calendar", "v3", credentials=creds)

        colors = service.colors().get().execute()

        print()
        print_color_square("#888888", 15)
        print(" Calendar colors: ", end="")
        print_color_square("#888888", 15)
        print()
        for cid, color in colors['calendar'].items():
            print(f"ID: {cid:<3} │ {'':<2}NAME: ", end="")
            print_color_square(color['background'])
            print(f" {CALENDAR_COLOR_NAMES[cid]:<14} │ {'':<2}BG: {color['background']} ", end="")
            print_color_square(color['background'])
            print(f"{'':<2} │ {'':<2}FG: {color['foreground']} ", end="")
            print_color_square(color['foreground'])
            print()

        print()
        print_color_square("#888888", 15)
        print(" Event Colors: ", end="")
        print_color_square("#888888", 15)
        print()
        for cid, color in colors['event'].items():
            print(f"ID: {cid:<3} │ {'':<2}NAME: ", end="")
            print_color_square(color['background'])
            print(f" {EVENT_COLOR_NAMES[cid]:<14} │ {'':<2}BG: {color['background']} ", end="")
            print_color_square(color['background'])
            print(f"{'':<2} │ {'':<2}FG: {color['foreground']} ", end="")
            print_color_square(color['foreground'])
            print()

        print()
        print_color_square("#888888", 15)
        print(" Available calendars: ", end="")
        print_color_square("#888888", 15)
        print()
        page_token = None
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                print(f"│ Name: {calendar_list_entry['summary']}")
                print(f"│ ID: {calendar_list_entry['id']}")
                print()
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break




    except HttpError as error:
        print(f"An error occurred: {error}")