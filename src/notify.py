import PySimpleGUI as sg
import sys

# sg.popup_notify("Hi, this popup is non-blocking notify\nand will take 10s to close.\nAt the same time, printing of time is still going !", display_duration_in_ms=10000)

# 0 is the name of the file !
sel = sys.argv[1]
exe_path = sys.argv[2]
# sg.SystemTray.notify(f"opening {sel}", exe_path, display_duration_in_ms=300, fade_in_duration=100)
sg.SystemTray.notify(f"opening {sel}", exe_path, fade_in_duration=100)
