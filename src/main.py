#!/usr/bin/python3

import PySimpleGUI as sg
import time

# sg.theme('DarkAmber')
# sg.theme('darkblue13')
sg.theme('darkred')
# sg.theme_previewer()

from layout import layout
from searchable_programs import get_all_progs_list, launch_app

programs_list = get_all_progs_list()
#  currently only showing programs whose exe_paths can be found
default_names = [p.replace(".lnk", "") for p in programs_list.keys() if programs_list[p] != ""]

current_names = default_names.copy()

# creating the window
# window = sg.Window("Hello World", layout=layout)
window = sg.Window("Py-Win-Launcher !",
									layout,
									return_keyboard_events=True,
									font="fixedsys 18",
									# dont use it because then it will always say on top , even whem it makes a popup
									# keep_on_top=True,
									)

# todo: sg.Window() read all params, finalize, location, font
# window.TKroot.focus_force() # doesnt work 

while True:
	event, values = window.read();
	"""event: `_name` for update in _name Input field ! | on enable_events=True """
	"""event: `file_name` for update in FileBrowse field with `key=file_name` ! | on enable_events=True """
	if event == sg.WIN_CLOSED:
			break
	elif event == "app_search_input":
		# call get_all_progs_list & update the gui
		val = values.get("app_search_input")
		if val == "":
			current_names = default_names
		else:
			# search the names and find the matching ones !
			current_names = [n for n in default_names if n.lower().startswith(val.lower())]
		window["-select-box-"].update(current_names)
		
	elif event == "-select-box-":
		# user has selected an app !
		sel = values.get("-select-box-")[0]
		exe_path = programs_list[f'{sel}.lnk']
		sg.popup(f"opening {sel} !\n{exe_path}!")

		process = launch_app(exe_path)
		# we need to call .poll because .poll() SETS & returns the return code
		# time.sleep(0.5) # i suspected right !!!!! it doesnt return till then !
		# # ! sleep call is still not perfect apps can take longer and it will still be none!
		# rt_code = None
		# while rt_code == None:
		# 	time.sleep(1)
		# 	rt_code = process.poll()
		process.wait()
		rt_code = process.poll()
		if not rt_code == 0:
			#! got 255 but it still worked mechakeys ?
			# program did not run correctly !
			sg.popup(f"Could not open {sel} {rt_code}!\n<check logs for more info>")
	else:
		# keyboard events, usable coz we have set return_keyboard_events=True
		if len(event) == 1:
			window["-out-"].update(value='%s - %s' % (event, ord(event)))
			# ! ok here we should just add these chars to search bar input & focus it !
		else:
			# Down:40, Up:38, Left:37, Right:39, MouseWheel:Up, MouseWheel:Down
			window["-out-"].update(f"{event}")

print("EXITING !")
window.close();


"""
CHANGELOG

gui changes, font, element removed
	fixedsys font looks cool !
encounted return code problems, not responding problems Fixed all !
found a way to get keyboard input


to add

scroll currently_focused_app using Down and Up
ctrl + `+/-` to adjust font size !
"""