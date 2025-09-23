import os
import sys


def set_background(hex):
    """Set background color using a hex code."""
    r, g, b = parseRGB(hex)
    print(f"\x1b[48;2;{r};{g};{b}m", end="")


def set_foreground(hex):
    """Set foreground color using a hex code."""
    r, g, b = parseRGB(hex)
    print(f"\x1b[38;2;{r};{g};{b}m", end="")


def parseRGB(hex_color):
    """
    Converts hexadecimal string to decimal 0-255 r,g,b values. Accepts shortened 3 char version and normal 6 char.
    """
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        r = int(hex_color[0:1], 16) * 16
        g = int(hex_color[1:2], 16) * 16
        b = int(hex_color[2:3], 16) * 16
        return r, g, b
    elif len(hex_color) == 6:
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return r, g, b

    return 0, 0, 0


def reset_formatting():
    """Reset ANSI formatting."""
    print("\x1b[0m", end="")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def header(title):
    set_foreground("#00ffff")
    print(f"{title}".center(50, "="))
    reset_formatting()
    print()


def get_key():
    """
    Wait for a key press and return:
      "UP" for up arrow,
      "DOWN" for down arrow,
      "ENTER" for the Enter key.
    """
    if os.name == "nt":
        # Use msvcrt for Windows
        import msvcrt

        key = msvcrt.getch()
        print(key)
        if (
            key == b"\xe0"
            or key == b"\x00"  # xe0 for cmd and x00 for integrated terminal
        ):  # Arrow keys are prefixed with an escape code.
            key2 = msvcrt.getch()
            print(key2)
            if key2 == b"H":
                return "UP"
            elif key2 == b"P":
                return "DOWN"
        elif key == b"\r":
            return "ENTER"
        elif key == b"\x03":
            sys.exit(0)
        return None
    else:
        # Unix-like: set terminal to raw mode and read bytes
        import tty, termios

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = os.read(fd, 3)  # Arrow keys are typically 3 bytes.
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        if ch == b"\x1b[A":
            return "UP"
        elif ch == b"\x1b[B":
            return "DOWN"
        elif ch in [b"\r", b"\n"]:
            return "ENTER"
        return None
