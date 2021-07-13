import sys
import os

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
	# os.listdir -> lists all files in dir 
	# os.walk ?
	# os.path.join
	# os.readlink

	lst = []

	for dirpath, _dirnames, files in os.walk(lnks_dir_path):
			# print(f'Found directory: {dirpath}')
			# files dont include folders !
			for file_name in files:
					abs_path = os.path.join(dirpath, file_name)
					print(abs_path)
					try:
						exe_path = os.readlink(abs_path)
						# ok so i cant manage to read the real path of .lnk sym link files using
						# os.readlink or os.path.realpath
						# btw this must be very interesting
						# https://stackoverflow.com/a/28952464/9596267
						lst.append((file_name, exe_path))
					except OSError as error:
						# should be OSError [WinError 4390]
						'''
						# [WinError 4390] not a reparse point !
						A reparse point is what linux calls a symbolic link.  It is actually similar to
						a shortcut or link that people use all the time.  An icon on your desktop is
						not really the program that it launches - it is simply a file that points to
						that program and tells it to launch when you click it.  A reparse point is the
						same concept except at the OS level instead of the user level.  In Windows 7,
						the easiest way to see an example of this is to open a command prompt and type
						dir /a and press enter.  You will see several entries that say junction and it
						will show you what they point to (junction point is another name for reparse
						point)
						'''
						print(file_name, error)
						pass
						# print(type(error)) -> <class 'OSError'> | how to people handle these logs ? like how do you get to know if its atually a string, tuple or a dict ???
						# todo handle NotImplementedError
	return lst

if __name__ == "__main__":
	# first arg is name of file !
	if sys.argv[1] == "test":
		print("testing !")
		print(get_all_progs_list())