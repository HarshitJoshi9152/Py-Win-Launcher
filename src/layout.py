import PySimpleGUI as sg
from searchable_programs import get_all_progs_list

programs_list = get_all_progs_list()
#? currently only showing programs whose exe_paths can be found
names = [p.replace(".lnk", "") for p in programs_list.keys() if programs_list[p] != ""]

layout = [
	[sg.Text("App launcher !")],
	[sg.In(key="app_search_input", enable_events=True)],
	[sg.Listbox(names, size=(40, len(names)), key='-select-box-', enable_events=True)],
	# [sg.FileBrowse(key="file_name", enable_events=True)],
	# [sg.Button("OK"), sg.Button("debug")],
	# [sg.Text('_'*40)], # horizontal_seperator
	# ? ok so out size is equal to the original text size unless explicity stated
	# [sg.Text("Output :"), sg.Text("", key="-out-", size=(40, 2))],
	# [sg.Text("Default value !",size=(40,4), key="debug_log")],
]

"""
red_button = b'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'

layout = [  [sg.Text('My Window')],
            [sg.Input(key='-IN-'), sg.Text('', key='-OUT-')],
            [sg.Button('Exit', image_data=red_button, button_color=('white', sg.COLOR_SYSTEM_DEFAULT), border_width=0)]  ]
"""

# gs.Column , sg.VSeperator