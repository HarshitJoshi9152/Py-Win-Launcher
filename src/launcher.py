# Script to watch main.py and relaunch GUI on file change !
#to be ran in a unix shell environment
#! but if i use this script i cant see the print logs in real time !


import os
import subprocess
import time

filename = "./main.py"
# filename = "/c/backup/Documents/html/javaScript/projects/win-launcher/src/main.py"

# todo: add watching multiple files !
# files_to_watch = ["./main.py", "./layout.py"]

cli = ["python", filename]

# watch file for changes
process = None;
last_time = None
while True:
	# great everything works !!
	t = os.stat(filename).st_mtime
	print(t)
	if t != last_time:
		if process:
			process.kill()
		# restart the process
		process = subprocess.Popen(cli)
		last_time = t
	# idk if this sleep call is really required !
	time.sleep(1)



"""
subprocess.Popen
	process.pid, .kill, .terminal (graceful shutdown, can be ignored !)

why doesnt a process spawned with Popen(cmd, shell=True) get terminated/killed when .kill/.terminated is called
	https://stackoverflow.com/a/13143013/9596267
	https://stackoverflow.com/questions/21936597/blocking-and-non-blocking-subprocess-calls
"""