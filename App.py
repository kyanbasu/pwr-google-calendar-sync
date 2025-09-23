import os
from windows.windowManager import change_window, main_loop, Window

# Enable ANSI escape codes on Windows
if os.name == "nt":
    from ctypes import byref, windll
    from ctypes.wintypes import DWORD

    ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
    STD_OUTPUT_HANDLE = -11
    h = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    mode = DWORD()
    windll.kernel32.GetConsoleMode(h, byref(mode))
    mode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
    windll.kernel32.SetConsoleMode(h, mode)


if __name__ == "__main__":
    change_window(Window.main)
    while True:
        main_loop()
