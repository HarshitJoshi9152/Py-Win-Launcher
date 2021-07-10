# Script to watch main.py and relaunch GUI on file change !
#to be ran in a unix shell environment
#! but if i use this script i cant see the print logs in real time !

import os
import subprocess
import time

file_to_run = "./main.py"
cli = ["python", file_to_run]
files_to_watch = ["./main.py", "./layout.py"]

# watch file for changes
process = None;
last_time = {}

while True:
	# looping over files we need to watch to find if they have changed based on their modified time !
	to_refresh = False
	for file in files_to_watch:
		# since we cant call break #29 we are using this hack to avoid extra work!
		if to_refresh:
			pass
		
		t = os.stat(file).st_mtime
		# every files last modified time is diff !
		if t != last_time.get(file):
			to_refresh = True
			last_time[file] = t
			#29 cant call break here ig it will quit the main while loop !

	if to_refresh:
		if process:
			process.kill()
		# restart the process
		process = subprocess.Popen(cli)
	# not really required but results in lower CPU usage !
	time.sleep(1)

# idle cpu usage stats
# thread, current CPU cons %  ,avg % of CPU consumption
# without: sleep ------> 4  , 25, 24
# with sleep ----------> 2-4,  0, 0.00


"""
subprocess.Popen
	process.pid, .kill, .terminal (graceful shutdown, can be ignored !)

why doesnt a process spawned with Popen(cmd, shell=True) get terminated/killed when .kill/.terminated is called
	https://stackoverflow.com/a/13143013/9596267
	https://stackoverflow.com/questions/21936597/blocking-and-non-blocking-subprocess-calls
"""