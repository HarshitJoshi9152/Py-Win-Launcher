#!/usr/bin/python3

import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import T
import subprocess
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

# val:names_list | WORKS ! | WOULD BE BETTER IF THIS WAS JUST VAL:NAME_INDEX
scroll_state_names = {}

# creating the window
# window = sg.Window("Hello World", layout=layout)
window = sg.Window("Py-Win-Launcher !",
									layout,
									return_keyboard_events=True,
									font="fixedsys 18",
									finalize=True,
									# location=(320,50),
									# size=(700, 518),
									resizable=True,
									# dont use it because then it will always say on top , even whem it makes a popup
									# keep_on_top=True,
									)
window["-dim-"].update(f"{window.CurrentLocation()} {window.size}")
# nice ! use element.Widget. to access tkinter
window["-select-box-"].Widget.config(cursor="hand2")
window["-select-box-"].Widget.itemconfig(0, fg='red', bg='light blue')
# https://pysimplegui.readthedocs.io/en/latest/call%20reference/#window
# window.use_custom_titlebar
# window.maximize()
# window.ding()
# todo: sg.Window() read all params, finalize, location, font
# window.TKroot.focus_force() # doesnt work 
# window.use_custom_titlebar(sg.Text("title bar !"))
# force_focus

# window.bring_to_front()
# window.get_screen_dimensions(), window.get_screen_size() for the entire screen dimensions!
# CurrentLocation -> location | now how do i detect motion ?
# window["-dim-"].update(window.CurrentLocation())

# hand2, arrow
# ? change cursor icon on scroll lol
# cursors = ["X_cursor", "arrow", "based_arrow_down", "based_arrow_up", "boat", "bogosity", "bottom_left_corner", "bottom_right_corner", "bottom_side", "bottom_tee", "box_spiral", "center_ptr", "circle", "clock", "coffee_mug", "cross", "cross_reverse", "crosshair", "diamond_cross", "dot", "dotbox", "double_arrow", "draft_large", "draft_small", "draped_box", "exchange", "fleur", "gobbler", "gumby", "hand1", "hand2", "heart", "icon", "iron_cross", "left_ptr", "left_side", "left_tee", "leftbutton", "ll_angle", "lr_angle", "man", "middlebutton", "mouse", "pencil", "pirate", "plus", "question_arrow", "right_ptr", "right_side", "right_tee", "rightbutton", "rtl_logo", "sailboat", "sb_down_arrow", "sb_h_double_arrow", "sb_left_arrow", "sb_right_arrow", "sb_up_arrow", "sb_v_double_arrow", "shuttle", "sizing", "spider", "spraycan", "star", "target", "tcross", "top_left_arrow", "top_left_corner", "top_right_corner", "top_side", "top_tee", "trek", "ul_angle", "umbrella", "ur_angle", "watch", "xterm"]
# cursorIndex = 0
# cursor = cursors[cursorIndex]
# window.set_cursor(cursor)
# window["-dim-"].update(f"{window.CurrentLocation()} {window.size} {cursor}")

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
	# elm_ids = ["-SEARCH-", "-select-box-", "-out-"]
	# for id in elm_ids:
	# 	window[id].update(window[id].get(), font=font)
	#! ok so we can only specify font on text nodes !
	elm_id = "head"
	window[elm_id].update(window[elm_id].get(), font=font)
	# ? ListBox has get_list_values method !

# but this makes the app go not responding !
def start_app(exe_path):
	# ! DAMN PERFECT EXAMPLE OF BLOCKING !
	# sg.popup(f"opening {sel} !\n{exe_path}!")
	# ? show app icon=base64_icon_str ?
	subprocess.Popen(["python","./notify.py", sel, exe_path])
	# sg.SystemTray.notify(f"opening {sel}", exe_path, display_duration_in_ms=300, fade_in_duration=100)
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
	event, values = window.read(33); # is there any advantage to using timeout ?
	"""event: `_name` for update in _name Input field ! | on enable_events=True """
	"""event: `file_name` for update in FileBrowse field with `key=file_name` ! | on enable_events=True """
	if event == sg.WIN_CLOSED:
			break

	elif event == "-SEARCH-":
		# call get_all_progs_list & update the gui
		val = values.get("-SEARCH-").strip()
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
		if len(window["-select-box-"].get_list_values()) > 0:
			window["-select-box-"].Widget.itemconfig(0, fg='red', bg='light blue')
		
	elif event == "-select-box-":
		# user has selected an app !
		if len(values.get("-select-box-")) > 0:
			sel = values.get("-select-box-")[0]
			exe_path = programs_list[f'{sel}.lnk']
			start_app(exe_path)

	elif event == "__TIMEOUT__":
		continue
	else:
		update_buffer(event)
		# keyboard events, usable coz we have set return_keyboard_events=True
		# idtkink we need the first if statement
		if event == "equal:187":
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
			#! WELL RESETING THE LIST WAS PRETTY DUMB ? HUH ? IF I COULD SCROLL ?
			#! we dont want to reset the list 
			if current_names == [] or window.find_element_with_focus() == window["-select-box-"]:
				continue
			val = values.get("-SEARCH-")
			# print("current_names", current_names)
			new_names = list(current_names[1:])
			new_names.insert(len(new_names), current_names[0])
			current_names = tuple(new_names)
			scroll_state_names[val] = new_names
			window["-select-box-"].update(new_names)
			listbox = window["-select-box-"]
			index = listbox.GetIndexes()[0] if listbox.GetIndexes() else 0 # else index on item currently scrolled !
			listbox.Widget.itemconfig(index, fg='red', bg='light blue')
		elif event == "Up:38":
			# todo: fix badcode
			if current_names == [] or window.find_element_with_focus() == window["-select-box-"]:
				# this is for the situation of searches that dont match !
				continue
			val = values.get("-SEARCH-")
			new_names = list(current_names[:-1])
			new_names.insert(0, current_names[-1])
			current_names = tuple(new_names)
			scroll_state_names[val] = new_names
			window["-select-box-"].update(new_names)
			listbox = window["-select-box-"]
			index = listbox.GetIndexes()[0] if listbox.GetIndexes() else 0 # else index on item currently scrolled !
			listbox.Widget.itemconfig(index, fg='red', bg='light blue')
		elif event == "\r":
			sel = current_names[0]
			exe_path = programs_list[f'{sel}.lnk']
			# launch_app(exe_path)
			start_app(exe_path)
		# ? change cursor icon on scroll lol
		# elif event == "MouseWheel:Down":
		# 	cursorIndex += 1
		# 	cursor = cursors[cursorIndex % len(cursors)]
		# 	window.set_cursor(cursor)
		# 	window["-dim-"].update(f"{window.CurrentLocation()} {window.size} {cursor}")
		# elif event == "MouseWheel:Up":
		# 	cursorIndex -= 1
		# 	cursor = cursors[cursorIndex % len(cursors)]
		# 	window.set_cursor(cursor)
		# 	window["-dim-"].update(f"{window.CurrentLocation()} {window.size} {cursor}")
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

highlighting works without any need of an event trigger.
changed cursor to hand2 for ListBox
native scrolling fixed !

-------------------------------- 

to add

elastic search !
ctrl + `+/-` to adjust font size !
> commands
file, edit Menu

exp

try Combo element sometime !
should i remove the onClick and add multiple selection option and highlighting and just use enter both ways
(we will have to bind_return on the ListBox)

ISSUES

WAIT WHAT ARE 2 WINDOWS BEING LAUNCHED ?
ALSO NOT RESPONDING BUG IS HERE !
	BETTER THAN BEFORE BUT STILL A BUG WITH MANY APPS !
	IT LAGS WHENEVER I START SOMETHING THAT TAKES A BIT MORE TIME TO LAUNCH
	IT GOES NOT RESPONDING, FOR SOMETIME 

	WAIT TRY INTERACTING WITH IT IMMEDIATELY AFTER LAUNCHING AN APP
		YA ITS FEARFUL ACT
	ALSO TIMEOUT DOESNT HELP LMAO !

	WAIT SOMETIMES ITS BECAUSE OF THE APP THAT WE ARE TRYING TO START,
	COZ WE ARE WAITING FOR IT YES !!!! THAT MUST BE IT

	maybe not, maybe some times it just doesnt return until the app ends !
"""