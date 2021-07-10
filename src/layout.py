import PySimpleGUI as sg;

layout = [
	[sg.Text("Hello from PySimpleGUI")],
	[sg.In(key="_name", enable_events=True)],
	[sg.FileBrowse(key="file_name", enable_events=True)],
	[sg.Button("OK"), sg.Button("debug")],
	# [sg.Text('_'*30)], # horizontal_seperator
	[sg.Text("Default value !",size=(40,4), key="debug_log")]
]
