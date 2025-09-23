import os
import sys


def set_background(hex_color):
    """Set background color using a hex code."""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    print(f"\x1b[48;2;{r};{g};{b}m", end="")


def set_foreground(hex_color):
    """Set foreground color using a hex code."""
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    print(f"\x1b[38;2;{r};{g};{b}m", end="")


def reset():
    """Reset ANSI formatting."""
    print("\x1b[0m", end="")


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
            return "CTRLC"
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
