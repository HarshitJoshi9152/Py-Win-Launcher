#!/usr/bin/python3

import PySimpleGUI as sg

sg.theme('DarkAmber')

layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Input(key="_name")], [sg.Button("OK")]]


# creating the window
# window = sg.Window("Hello World", layout=layout)
window = sg.Window("Hello World", layout=layout, margins=(400, 300))


while True:
	event, values = window.read();
	if event == sg.WIN_CLOSED:
			break
	elif event == "OK":
		print(f"Hello {values['_name']} !")

window.close();