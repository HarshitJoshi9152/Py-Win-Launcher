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

# val:names_list | WORKS !
scroll_state_names = {}

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
buffer_max_len = 6
def update_buffer(key):
	global buffer
	if len(buffer) >= buffer_max_len:
		buffer.pop(0)
	buffer.append(key)

def query_buffer(keys_lst):
	global buffer
	return keys_lst == buffer[len(buffer) - len(keys_lst):]

size = 18
def update_font(font):
	# elm_ids = ["app_search_input", "-select-box-", "-out-"]
	# for id in elm_ids:
	# 	window[id].update(window[id].get(), font=font)
	#! ok so we can only specify font on text nodes !
	id = "head"
	window[id].update(window[id].get(), font=font)

# but this makes the app go not responding !
def start_app(exe_path):
	# ! DAMN PERFECT EXAMPLE OF BLOCKING !
	# sg.popup(f"opening {sel} !\n{exe_path}!")
	# ? show app icon=base64_icon_str ?
	sg.SystemTray.notify(f"opening {sel}", exe_path, display_duration_in_ms=300, fade_in_duration=100)
	# sg.SystemTray.notify(f"opening {sel}", exe_path)
	# ! how do i make this think non blocking

	# p = Thread(target=sg.SystemTray.notify, args=[f"opening {sel}", exe_path])
	# p.start()
	
	process = launch_app(exe_path)
	process.wait()
	rt_code = process.poll()
	if not rt_code == 0:
		# program did not run correctly !
		sg.popup(f"Could not open {sel} {rt_code}!\n<check logs for more info>")


while True:
	event, values = window.read(); # is there any advantage to using timeout ?
	"""event: `_name` for update in _name Input field ! | on enable_events=True """
	"""event: `file_name` for update in FileBrowse field with `key=file_name` ! | on enable_events=True """
	if event == sg.WIN_CLOSED:
			break

	elif event == "app_search_input":
		# call get_all_progs_list & update the gui
		val = values.get("app_search_input").strip()
		if scroll_state_names.get(val):
			current_names = scroll_state_names[val]
			if (scroll_state_names[val] == []): # this cant be iguess BUT IT HAPPENS ON NOT FOUND SEARCHES 
				print("YES THIS IS THE FOURN")
		elif val == "":
			current_names = default_names
		else:
			# search the names and find the matching ones !
			current_names = [n for n in default_names if n.lower().startswith(val.lower())]
		window["-select-box-"].update(current_names)
		
	elif event == "-select-box-":
		# user has selected an app !
		sel = values.get("-select-box-")[0]
		exe_path = programs_list[f'{sel}.lnk']
		start_app(exe_path)

	elif event == "__TIMEOUT__":
		continue
	else:
		update_buffer(event)
		# keyboard events, usable coz we have set return_keyboard_events=True
		# idtkink we need the first if statement
		if len(event) == 1237123788721378: # to prevent `\r` getting caught here
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
			# sg.show_debugger_popout_window()
		elif event == "Down:40":
			# todo: fix badcode
			if current_names == []:
				continue
			val = values.get("app_search_input")
			print("current_names", current_names)
			new_names = list(current_names[1:])
			new_names.insert(len(new_names), current_names[0])
			current_names = tuple(new_names)
			scroll_state_names[val] = new_names
			window["-select-box-"].update(new_names)
			pass
		elif event == "Up:38":
			# todo: fix badcode
			if current_names == []:
				# this is for the situation of searches that dont match !
				continue
			val = values.get("app_search_input")
			new_names = list(current_names[:-1])
			new_names.insert(0, current_names[-1])
			current_names = tuple(new_names)
			scroll_state_names[val] = new_names
			window["-select-box-"].update(new_names)
			pass
		elif event == "\r":
			sel = current_names[0]
			exe_path = programs_list[f'{sel}.lnk']
			# launch_app(exe_path)
			start_app(exe_path)
		else:
			# Down:40, Up:38, Left:37, Right:39, MouseWheel:Up, MouseWheel:Down
			window["-out-"].update(f"{buffer}")
			# window["-out-"].update(f"{event}")
		# print(event)
		matches = query_buffer([1, 2])

print("EXITING !")
window.close();


"""
CHANGELOG


added stateful scrolling ! but am i even going to use it ?
	doesnt work on keydown,
enter to launch the app shown on first no !
better search


to add

elastic search !
scroll currently_focused_app using Down and Up
ctrl + `+/-` to adjust font size !

issues

app launching, showing the notifications and popups are blocking the code execution !

does the window sometimes become not responding ?
after launching an app ?
"""