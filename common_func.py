import platform
import subprocess
import glob
import os
import sys
import serial
from xml.etree import ElementTree
settings_xml_string="<settings>\n<setting type=\"programmer_name\" value=\"USBasp\" />\n</settings>"
def split_filepath(path_to_split):
	return_path=[]
	if IsWin()==True:
                path_to_split=path_to_split.replace("/",chr(92))
		last_pos=path_to_split.rfind(chr(92))
	else:
		last_pos=path_to_split.rfind('/')
			
	split1=path_to_split[0:last_pos]
	split2=path_to_split[last_pos+1:]
	return_path.append(split1)
	return_path.append(split2)
	return return_path
def open_terminal_hex_dir(filename_str):
	if IsWin()==True:
		last_pos=filename_str.rfind(chr(92))
	else:
		last_pos=filename_str.rfind('/')
			
	outstr=filename_str[0:last_pos]
	if IsWin()==True:
		os.system('cmd /k '+chr(34)+outstr+chr(34))
	if IsLinux()==True:
		comm_str='gnome-terminal --working-directory='+chr(34)+outstr+chr(34)
		print comm_str
		os.system(comm_str)

def get_config(config_to_find):
	if os.path.exists("settings.xml")==False:
		return False	
	xmlparserobj=ElementTree.parse("settings.xml")
	xmlroot=xmlparserobj.getroot()
	for node in xmlroot.findall("setting"):
		type_setting=node.get("type")
		if type_setting==config_to_find:
			return node.get("value")	
	return ""

def set_config(config_to_set,config_value):
	ret_str=0
	if os.path.exists("settings.xml")==False:
		with open("settings.xml","w") as file_handler:
			file_handler.write(settings_xml_string)
			ret_str=1
	xmlparserobj=ElementTree.parse("settings.xml")
	xmlroot=xmlparserobj.getroot()
	for node in xmlroot.findall("setting"):
		type_setting=node.get("type")
		if type_setting==config_to_set:
			node.set("value",config_value)
			break
	xmlparserobj.write("settings.xml")
	return ret_str
	
def get_programmer():
	return_list=[]
	programmer_name=get_config("programmer_board")
	if programmer_name==False or len(programmer_name)==0:
		programmer_name="USBasp"
		return_list.append("Settings file not found or corrupted.It has been reset to default.")
	return_list.append(programmer_name)
	return return_list
	
def process_msg(msg_str):
	if msg_str.find("could not find")>=0:
		return "Could not locate device.Check connections"
	if msg_str.find("target doesn't answer")>=0:
		return "Chip not found"
	if msg_str.find("Yikes")>=0:
		return "Invalid device signature.Check chip connections"
	if msg_str.find("written")>=0 and msg_str.find("verified")>=0:
		return "AVR successfully written."
	if msg_str.find("written")<0 and msg_str.find("verified")>=0:
		return "AVR successfully verified."
	if msg_str.find("failed")<0 and msg_str.find("writing output file")>=0:
		return "AVR successfully read."
	
	return ""
	
def run_command_capture(comstr,nomod=False,wdir=""):
	try:
		if nomod==False:
			compar=comstr.split(" ")
		else:
			compar=comstr
		print compar
		if IsMac()==True:
			compar[0]='/usr/local/CrossPack-AVR/bin/avrdude'
		
		if len(wdir)>0:
			os.chdir(wdir)
		if IsWin()==False:
                        proc = subprocess.Popen(compar, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,shell=False)
                        tmp = proc.stdout.read()
                else:
                        p = subprocess.Popen(compar,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        tmp,err = p.communicate()
		return tmp
	except Exception,e:
		print str(e)
		return "err:"+str(e)
		
		
def get_programmer_details(board_name):
	xmlparserobj=ElementTree.parse("programmer_boards.xml")
	xmlroot=xmlparserobj.getroot()
	retlist=[]
	for node in xmlroot.findall("dev"):
		type_board=node.get("type")
		name_board=node.find("name").text
		if name_board==board_name:
			protocol=node.find("protocol").text
			interface=node.find("interface").text
			retlist.append(node.find("protocol").text)
			if interface=="serial":
				retlist.append(node.find("speed").text)
	return retlist

def get_os():
	return platform.system()
	
def IsWin():
	retval=get_os()
	if(retval.find("Windows")>=0):
		return True
	else:
		return False
		
def IsLinux():
	retval=get_os()
	if(retval.find("Linux")>=0):
		return True
	else:
		return False

def IsMac():
	retval=get_os()
	if(retval.find("Darwin")>=0):
		return True
	else:
		return False

def list_serial_ports():
    if IsWin()==True:
        # Scan for available ports.
        available = []
        for i in range(256):
            try:
                s = serial.Serial(i)
                available.append('COM'+str(i+1))
                s.close()
            except serial.SerialException:
                pass
        return available
    elif IsMac()==True:
        # Mac
        return glob.glob('/dev/tty*') + glob.glob('/dev/cu*')
    elif IsLinux()==True:
        # Assume Linux or something else
        return glob.glob('/dev/ttyS*') + glob.glob('/dev/ttyUSB*')+glob.glob('/dev/ttyACM*')

