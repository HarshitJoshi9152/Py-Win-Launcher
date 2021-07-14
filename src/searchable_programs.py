import sys
import os
import subprocess
from exp import get_real_path


r'''
windows start menu uses folders
C:\Users\<account>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs (For its Individual users) 
&
C:\ProgramData\Microsoft\Windows\Start Menu\Programs (For All its users.)

to store `.ink` files pointing to the exes !


$	file IDLE (Python 3.7 32-bit).lnk | wrap  
>	IDLE (Python 3.7 32-bit).lnk: MS Windows shortcut, Item id list present, Points
	to a file or directory, Has Description string, Has Relative path, Has Working
	directory, Has command line arguments, Icon number=0, Archive, ctime=Tue Jun 26
	17:08:42 2018, mtime=Sat Aug 11 00:39:16 2018, atime=Tue Jun 26 17:08:42 2018,
	length=95896, window=hide
'''

#! SHOULD I MAKE A CLASS ?

username = os.getlogin() or os.getenv("username")
lnks_dir_path = os.path.join(R"C:\Users", username, R"AppData\Roaming\Microsoft\Windows\Start Menu\Programs")
# BUT THIS IS LANGUAGE DEPENDENT ! WHAT ABOUT GERMANY COPY OF WINDOWS ?

def get_all_progs_list():
	""" get_all_progs_list
			returns a list of tuples with items as ($name_of_prog, $path_of_executable)
	"""
	lst = {}
	for dirpath, _dirnames, files in os.walk(lnks_dir_path):
			# print(f'Found directory: {dirpath}')
			# files dont include folders !
			for file_name in files:
					if not file_name.endswith(".lnk"):
						continue
					abs_path = os.path.join(dirpath, file_name)
					# print(abs_path)
					exe_path = ""
					try:
						exe_path = os.readlink(abs_path)
						# print((file_name,exe_path ))
					except OSError as err:
						try:
							exe_path = get_real_path(abs_path)
						except ValueError as noValidPathFound:
							pass
					lst[file_name] = exe_path
					# if exe_path == "":
					# 	print(abs_path)
					# print(type(error)) -> <class 'OSError'> | how to people handle these logs ? like how do you get to know if its atually a string, tuple or a dict ???
	return lst

def launch_app(path):
	#? this needs path of a exe file ! RETURNS <subprocess.Popen object>
	cli = [path];
	# using shell=True to not allow launcher to close the app once opened !
	# * or os.system os.startfile !
	return subprocess.Popen(cli, shell=True)
	# killing the shell that spawns the process | NOT
	# process.kill(); ok so now .kill kills it ? ig it happens when its a terminal command not an exe ? idk

	#Attributes:
	#|      stdin, stdout, stderr, pid, returncode
	#Methods:
	#|			kill, terminate, communicate, send_signal, poll

if __name__ == "__main__":
	# first arg is name of file !
	if sys.argv[1] == "test":
		print("testing !")
		print(get_all_progs_list())
		# p = launch_app(R"C:\Program Files\Parsec\parsecd.exe")
		# print(p)