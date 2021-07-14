import struct
import os
# path = "C:\\Users\\ruby\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Parsec\\Parsec.lnk"

def get_lnk_path(path):
	# https://stackoverflow.com/a/28952464/9596267
	with open(path, 'rb') as stream:
		content = stream.read()
		# skip first 20 bytes (HeaderSize and LinkCLSID)
		# read the LinkFlags structure (4 bytes)
		lflags = struct.unpack('I', content[0x14:0x18])[0]
		position = 0x18
		# if the HasLinkTargetIDList bit is set then skip the stored IDList 
		# structure and header
		if (lflags & 0x01) == 1:
			position = struct.unpack('H', content[0x4C:0x4E])[0] + 0x4E
		last_pos = position
		position += 0x04
		# get how long the file information is (LinkInfoSize)
		length = struct.unpack('I', content[last_pos:position])[0]
		# skip 12 bytes (LinkInfoHeaderSize, LinkInfoFlags, and VolumeIDOffset)
		position += 0x0C
		# go to the LocalBasePath position
		lbpos = struct.unpack('I', content[position:position+0x04])[0]
		position = last_pos + lbpos
		# read the string at the given position of the determined length
		size= (length + last_pos) - position - 0x02
		temp = struct.unpack('c' * size, content[position:position+size])
		target = ''.join([chr(ord(a)) for a in temp])
		return target

# print(get_lnk_path("C:\\Users\\ruby\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Parsec\\Parsec.lnk"))
# C:\Program Files\Parsec\parsecd.exe

def get_real_path(lnk_path):
	with open(lnk_path, "rb") as f:
		content = f.read()
		# content = f.read().decode("utf-8")
		# filePath = re.findall("C:.*", content, flags=re.DOTALL)
		lnk_path = b""
		f.seek(0)
		# f.seek(0x1e0)
		# ? read file data 1 char at a time and filter out target path ! 
		while True:
			k = f.read(1)
			# when the file has been completely read fd.read return b'' (an empty byte)
			# alternatively get file length and complare current position with f.tell()
			if k == b'':
				break
			try:
				# k.decode("utf-8")
				# if k.startswith(b'\x00'):
				# print(f'{k}')
				# if f'{k}' in string.printable.split(''):
				# 	print("yes ", k)
				if f"{k}".startswith("b'\\x"):
					continue
				# if fr'{k}' == rb'\x' or k == b'L':
				# 	# we dont want to record these bytes
				# 	continue
				lnk_path += k
			except TypeError:
				print("ERROR !\n")
				break
		
		# THIS ENTIRE FILE FEELS LIKE THE WORST CODE THAT I HAVE ENVERY WRITTEN BUT THIS IS THE BEST I COULD HAVE DONE ON WINDOWS 7 PY 3.7 LMAO 
		records = []
		recording = False
		buffer = []
		for v, i in enumerate(f"{lnk_path}"):
			buffer.append(i)
			# print(i)
			# max limit is 4
			if (len(buffer) == 5):
				buffer.pop(0)
			# print("".join(buffer))
			if ("".join(buffer) == R"C:\\"):
				recording = True
				records.append(["C:\\"])
			elif ("".join(buffer) == ".exe"):
				# since buffer remains `\CHAR.ex` before& only becomes `.exe` when current char is `e`
				# & we stop the recording thats why we will have to add it ourself !
				if recording:
					records[len(records) - 1].append(i)
				recording = False
			if recording:
				records[len(records) - 1].append(i)
		
		# check for valid paths
		lnk_path = ""
		for rec in records:
			p = "".join(rec)
			try:
				os.stat(p)
				lnk_path = p
				break
			except OSError as err:
				continue
		if lnk_path == "":
			raise ValueError("NO VALID PATH FOUND ")
		return lnk_path

		# regex = b'[A-Z]:\\\\(?:[^\\\\\/:*?"<>]+\\\\)*[^\\\\\/:*?"<>]*;'
		# regex = b'[A-Z]:\\\\(?:[^\\\\\/:*?"<>]+\\\\)*[^\\\\\/:*?"<>]*.exe'
		# matches = re.findall(regex, path, flags=re.DOTALL)
		# if len(matches) == 0:
		# 	raise ValueError(f"REGEXP did not work !\n {path}")
		# return f"{matches[0]}".replace("b'", "").replace("'", "")


if __name__ == "__main__":
	# ? tests
	# res = get_real_path("C:\\Users\\ruby\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Parsec\\Parsec.lnk")
	# p = R"C:\Users\ruby\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\ZEIT, Inc\Hyper.lnk"
	p = R"C:\Users\ruby\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Discord Inc\Discord.lnk"
	res = get_real_path(p)
	print(res)