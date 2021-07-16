import sys
import PySimpleGUI as sg
import subprocess

sel = sys.argv[1]
exe_path = sys.argv[2]

# ig idk the diff btw shell=True & shell=False that deeply/accurately
# process = subprocess.Popen([exe_path], shell=True) # shell=True shows the launched app's logs in console !
process = subprocess.Popen([exe_path])
process.wait()
rt_code = process.poll()
# python process.poll() returns 4294967295 ?
if not rt_code == 0:
	# program did not run correctly !
	sg.popup(f"Could not open {sel} {rt_code}!\n<check logs for more info>")


# ----------------------------------- previous comments -----------------------------------
# process.kill(); ok so now .kill kills it ? ig it happens when its a terminal command not an exe ? idk
# Attributes:
# |      stdin, stdout, stderr, pid, returncode
# Methods:
# |			kill, terminate, communicate, send_signal, poll

#!well os.system returns the code on first try so maybe try that ? BUT THERE IS AN UGLY NOT WORKING MSG 
#! MAYBE WE DONT HAVE TO IMPLEMENT THE MSG OURSELF LMAO !

# * use subprocess.Popen or os.system os.startfile !