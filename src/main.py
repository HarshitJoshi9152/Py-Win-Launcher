#!/usr/bin/python3

import PySimpleGUI as sg

sg.theme('DarkAmber')

from layout import layout

# creating the window
# window = sg.Window("Hello World", layout=layout)
window = sg.Window("Hello World", layout=layout, margins=(400, 300))


while True:
	event, values = window.read();
	"""event: `_name` for update in _name Input field ! | on enable_events=True """
	"""event: `file_name` for update in FileBrowse field with `key=file_name` ! | on enable_events=True """
	if event == sg.WIN_CLOSED:
			break
	if event == "debug":
		# next line is not working
		window.Element("debug_log").update(f"event: {event}, values: {str(values)}")
		print(event);
		print(values)
	elif event == "OK":
		print(f"Hello {values['_name']} !")
	else:
		pass
		# print(event);
		# print(values)

print("EXITING !")
window.close();