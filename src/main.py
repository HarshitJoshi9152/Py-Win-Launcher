#!/usr/bin/python3

import PySimpleGUI as sg

# sg.theme('DarkAmber')
sg.theme('darkblue13')
# sg.theme_previewer()

from layout import layout
from searchable_programs import get_all_progs_list, launch_app

programs_list = get_all_progs_list()
#  currently only showing programs whose exe_paths can be found
names = [p.replace(".lnk", "") for p in programs_list.keys() if programs_list[p] != ""]

# creating the window
# window = sg.Window("Hello World", layout=layout)
window = sg.Window("Hello World", layout=layout)

while True:
	event, values = window.read();
	"""event: `_name` for update in _name Input field ! | on enable_events=True """
	"""event: `file_name` for update in FileBrowse field with `key=file_name` ! | on enable_events=True """
	if event == sg.WIN_CLOSED:
			break
	elif event == "app_search_input":
		# call get_all_progs_list & update the gui
		window["-out-"].update(values.get("app_search_input"), background_color="red")
		# window["-select-box-"].update(names)
	elif event == "-select-box-":
		# user has selected an app !
		sel = values.get("-select-box-")[0]
		exe_path = programs_list[f'{sel}.lnk']
		sg.popup(f"opening {sel} !\n{exe_path}!")
		process = launch_app(exe_path)
		print(process.returncode) # why always none !!!!
	elif event == "OK":
		print(f"Hello {values.get('_name')} !")
	elif event == "debug":
		# now we dont need to do window.Element to target an element !
		window.Element("debug_log").update(f"event: {event}, values: {str(values)}")
		print(event);
		print(values)
	else:
		pass
		# print(event);
		# print(values)

print("EXITING !")
window.close();