#!/usr/bin/python3

import PySimpleGUI as sg
# from multiprocessing import Process
# from threading import Thread

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
									finalize=True
									# dont use it because then it will always say on top , even whem it makes a popup
									# keep_on_top=True,
									)
# window.use_custom_titlebar
# window.maximize()
# todo: sg.Window() read all params, finalize, location, font
# window.TKroot.focus_force() # doesnt work 

buffer = []
buffer_max_len = 2
def update_buffer(key):
	global buffer
	if len(buffer) >= buffer_max_len:
		buffer.pop(0)
	buffer.append(key)

def query_buffer(keys_lst):
	global buffer
	return keys_lst == buffer[len(buffer) - len(keys_lst):]

def update_font(font):
	# elm_ids = ["app_search_input", "-select-box-", "-out-"]
	# for id in elm_ids:
	# 	window[id].update(window[id].get(), font=font)
	#! ok so we can only specify font on text nodes !
	id = "head"
	window[id].update(window[id].get(), font=font)

size = 18

while True:
	event, values = window.read(); # is there any advantage to using timeout ?
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
		# ! DAMN PERFECT EXAMPLE OF BLOCKING !
		# sg.popup(f"opening {sel} !\n{exe_path}!")
		# ? show app icon=base64_icon_str ?
		sg.SystemTray.notify(f"opening {sel}", exe_path, display_duration_in_ms=300, fade_in_duration=100)
		# ! how do i make this think non blocking
		# p = Process(target=sg.SystemTray.notify, args=[f"opening {sel}", exe_path])
		# p.start()
		process = launch_app(exe_path)
		process.wait()
		rt_code = process.poll()
		if not rt_code == 0:
			# program did not run correctly !
			sg.popup(f"Could not open {sel} {rt_code}!\n<check logs for more info>")
			continue
	elif event == "__TIMEOUT__":
		pass
	else:
		# keyboard events, usable coz we have set return_keyboard_events=True
		if len(event) == 1:
			window["-out-"].update(value='%s - %s' % (event, ord(event)))
			# ! ok here we should just add these chars to search bar input & focus it !
		elif event == "equal:187":
			size += 2
			# for key in window.keys():
			# 	try:
			# 		window[key].
			# ! some fonts may only change text size on certain font-size values
			update_font(f"fixedsys {size}")
		elif event == "minus:189":
			size -= 2
			update_font(f"fixedsys {size}")
		else:
			# Down:40, Up:38, Left:37, Right:39, MouseWheel:Up, MouseWheel:Down
			window["-out-"].update(f"{event}")
		update_buffer(event)
		window["-out-"].update(f"{buffer}")
		matches = query_buffer([1, 2])

print("EXITING !")
window.close();


"""
CHANGELOG

using sg.SystemTray.notify("hello ", "msg") instead of popup
tried to add key_buffer system to keep keystrokes in memory
tried to enable dynamically adjusting font size

to add

scroll currently_focused_app using Down and Up
ctrl + `+/-` to adjust font size !

issues

app launching, showing the notifications and popups are blocking the code execution !

does the window sometimes become not responding ?
after launching an app ?
"""