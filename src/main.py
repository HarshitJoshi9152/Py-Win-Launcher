#!/usr/bin/python3

import PySimpleGUI as sg
import time

# sg.theme('DarkAmber')
sg.theme('darkblue13')
# sg.theme_previewer()

from layout import layout
from searchable_programs import get_all_progs_list, launch_app

programs_list = get_all_progs_list()
#  currently only showing programs whose exe_paths can be found
default_names = [p.replace(".lnk", "") for p in programs_list.keys() if programs_list[p] != ""]

current_names = default_names.copy()

# creating the window
# window = sg.Window("Hello World", layout=layout)
window = sg.Window("Py-Win-Launcher !", layout=layout)

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
		time.sleep(1) # i suspected right !!!!! it doesnt return till then !
		rt_code = process.poll()
		if not rt_code == 0:
			# program did not run correctly !
			# http://youtube.com/watch?v=e1TR9Wq0QRs
			sg.popup(f"Could not open {sel} {rt_code}!\n<check logs for more info>")
	elif event == "OK":
		print(f"Hello {values.get('_name')} !")
	elif event == "debug":
		# now we dont need to do window.Element to target an element !
		window.Element("debug_log").update(f"event: {event}, values: {str(values)}")
		print(event)
		print(values)
	else:
		pass
		# print(event);
		# print(values)

print("EXITING !")
window.close();