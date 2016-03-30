import os
import sys
from PyQt4 import QtCore, QtGui
from frmmain import Ui_frmmain
from about_class import aboutbox
import common_func
import ext_stuffs
import avrdude
import functools
import arduino_handler


class mainform(QtGui.QMainWindow):
	global_chipname=""
	global_programmer=""
	is_arduino_board=False
	
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_frmmain()
		self.ui.setupUi(self)
		#self.ui.gpcs_chip.setStyleSheet('color: white')
		# here we connect signals with our slots
		QtCore.QObject.connect(self.ui.bttnterminal,QtCore.SIGNAL("clicked()"), self.bttnterminal_clk)
		QtCore.QObject.connect(self.ui.bttnbrowse,QtCore.SIGNAL("clicked()"), self.bttnbrowse_clk)
		QtCore.QObject.connect(self.ui.bttnwrite,QtCore.SIGNAL("clicked()"), self.write_to_chip)
		QtCore.QObject.connect(self.ui.bttnread,QtCore.SIGNAL("clicked()"), self.read_from_chip)
		QtCore.QObject.connect(self.ui.bttnverify,QtCore.SIGNAL("clicked()"), self.verify_from_chip)
		
		#QtCore.QObject.connect(self.ui.bttnprgsettings,QtCore.SIGNAL("clicked()"), self.bttnprgsettings_clk)
		QtCore.QObject.connect(self.ui.gpcs_chip,QtCore.SIGNAL("clicked()"), self.gpcschip_clk)
		
		QtCore.QObject.connect(self.ui.menuAbout,QtCore.SIGNAL("triggered()"), self.showaboutbox)
		#programmer buttons
		
		QtCore.QObject.connect(self.ui.actionUSBasp,QtCore.SIGNAL("triggered()"), functools.partial(self.select_programmer,'USBasp'))
		QtCore.QObject.connect(self.ui.actionAVRisp,QtCore.SIGNAL("triggered()"), functools.partial(self.select_programmer,'AVRisp/ArduinoISP'))
		
		self.set_programmer_init()
		
		
		
		self.load_arduino_menus()
		self.show_ports()
		
		#timer_test=QtCore.QTimer(self)
		
		#self.connect(timer_test,QtCore.SIGNAL("timeout()"),self.print_msg)
		#timer_test.start(1000)
		
	#Launches the terminal or command prompt	
	
	def set_programmer_init(self):
		programmer_name_list=common_func.get_programmer()
		
		if len(programmer_name_list)>1:
			QtGui.QMessageBox.critical(self,"Error:"+programmer_name_list[0])
			self.global_programmer=programmer_name_list[1]
			print common_func.set_config("programmer_board","USBasp")
		else:
			self.global_programmer=programmer_name_list[0]
		list_arduino=arduino_handler.get_arduino_list()
		try:
			index_element=list_arduino.index(self.global_programmer)
			if index_element>=0:
				self.global_chipname=arduino_handler.get_chipname(self.global_programmer)
				self.is_arduino_board=True
				self.ui.gpcs_chip.setText(self.format_chipname(self.global_chipname))
		except ValueError:
			self.ui.gpcs_chip.setText("")	
		programmer_details=common_func.get_programmer_details(self.global_programmer)
		if len(programmer_details)>1:
			self.ui.cbobaudrate.setText(programmer_details[1])	
		self.update_programmer_name()
		
	def update_programmer_name(self):
		self.ui.lblprg.setText(self.global_programmer)
		
	def load_arduino_menus(self):
		list_arduino=arduino_handler.get_arduino_list()
		for arduino_item in list_arduino:
			menu_arduino=self.ui.menuArduino_Boards.addAction(arduino_item)
			QtCore.QObject.connect(menu_arduino,QtCore.SIGNAL("triggered()"),functools.partial(self.select_programmer,arduino_item,True))
			self.ui.menuArduino_Boards.addAction(menu_arduino)
	
	def show_ports(self):
		self.ui.cboport.clear()
		self.ui.cboport.addItems(common_func.list_serial_ports())
	
	def verify_from_chip(self):
		#time for constructing the command string
		#first,check if we have a file
		splitted_path=common_func.split_filepath(str(self.ui.txtfilename.text()))
		str_filename=splitted_path[1]
		path_wd=splitted_path[0]
		if len(str_filename)==0:
			QtGui.QMessageBox.critical(self,"Error:", "No file has been selected.")
			return
		#if os.path.exists(os.path.abspath(str_filename))==False:
		#	QtGui.QMessageBox.critical(self,"Error:","The selected file doesnt exist.May be it has been deleted")
		#	return
		if len(self.global_chipname)==0:
			QtGui.QMessageBox.critical(self,"Error:","No chip detected")
			return
		cmd_str=[]
		#alright,we have a file.Now,time for constructing our command string
		#time to know what programmer are we using
		programmer_details=common_func.get_programmer_details(self.global_programmer)
		protocol=programmer_details[0]
		cmd_str.append("avrdude")
		cmd_str.append("-c")
		cmd_str.append(protocol)
		cmd_str.append("-p")
		cmd_str.append(self.global_chipname)
		
		#cmd_str="avrdude -c "+protocol+" -p "+self.global_chipname
		if len(programmer_details)>1:
			speed=str(self.ui.cbobaudrate.text())
			cmd_str.append("-P")
			cmd_str.append(str(self.ui.cboport.currentText()))
			cmd_str.append("-b")
			cmd_str.append(speed)
			
			#cmd_str=cmd_str+" -P "+str(self.ui.cboport.currentText())+" -b " + speed
		memtype=""
		#okay!we have programmer and parameters,now time to checkwhich memory is to be written
		if self.ui.rdoflash.isChecked():
			memtype="flash"
		if self.ui.rdoeeprom.isChecked():
			memtype="eeprom"
		cmd_str.append("-U")
		cmd_str.append(memtype + ":v:"+str_filename+":i")
		
		#cmd_str += " -U " + memtype + ":v:"+chr(34)+str_filename+chr(34)+":i"
		output_str=common_func.run_command_capture(cmd_str,True)
		self.ui.txtterminal.setText(output_str)
		output_msg=common_func.process_msg(output_str)	
		QtGui.QMessageBox.critical(self,"Message",output_msg)
		
	def read_from_chip(self):
		#time for constructing the command string
		#first,check if we have a file
		self.filename = QtGui.QFileDialog.getSaveFileName(self, "Save file", "", "Hex files (*.hex);;Bin Files(*.bin);;EEPROM files(*.eep);;All Files(*.*)")
		
		if len(self.filename)>0:
			splitted_path=common_func.split_filepath(str(self.filename))
		str_filename=splitted_path[1]
		path_wd=splitted_path[0]
		print str_filename
		if len(str_filename)==0:
			QtGui.QMessageBox.critical(self,"Error:", "No file has been set.Operation can't continue")
			return
		#if os.path.exists(os.path.abspath(str_filename))==False:
		#	QtGui.QMessageBox.critical(self,"Error:","The selected file doesnt exist.May be it has been deleted")
		#	return
		if len(self.global_chipname)==0:
			QtGui.QMessageBox.critical(self,"Error:","No chip detected")
			return
		cmd_str=[]
		#alright,we have a file.Now,time for constructing our command string
		#time to know what programmer are we using
		programmer_details=common_func.get_programmer_details(self.global_programmer)
		protocol=programmer_details[0]
		cmd_str.append("avrdude")
		cmd_str.append("-c")
		cmd_str.append(protocol)
		cmd_str.append("-p")
		cmd_str.append(self.global_chipname)
		
		if len(programmer_details)>1:
			speed=str(self.ui.cbobaudrate.text())
			cmd_str.append("-P")
			cmd_str.append(str(self.ui.cboport.currentText()))
			cmd_str.append("-b")
			cmd_str.append(speed)
		memtype=""
		#okay!we have programmer and parameters,now time to checkwhich memory is to be written
		if self.ui.rdoflash.isChecked():
			memtype="flash"
		if self.ui.rdoeeprom.isChecked():
			memtype="eeprom"
		cmd_str.append("-U")
		cmd_str.append(memtype + ":r:"+str_filename+":i")
		output_str=common_func.run_command_capture(cmd_str,True,path_wd)
		self.ui.txtterminal.setText(output_str)
		output_msg=common_func.process_msg(output_str)	
		QtGui.QMessageBox.critical(self,"Message",output_msg)
		
			
	def write_to_chip(self):
		#time for constructing the command string
		#first,check if we have a file
		splitted_path=common_func.split_filepath(str(self.ui.txtfilename.text()))
		str_filename=splitted_path[1]
		path_wd=splitted_path[0]
		print str_filename
		if len(str_filename)==0:
			QtGui.QMessageBox.critical(self,"Error:", "No file has been selected.")
			return
		#if os.path.exists(os.path.abspath(str_filename))==False:
		#	QtGui.QMessageBox.critical(self,"Error:","The selected file doesnt exist.May be it has been deleted")
		#	return
		if len(self.global_chipname)==0:
			QtGui.QMessageBox.critical(self,"Error:","No chip detected")
			return
		
		cmd_str=[]
		#alright,we have a file.Now,time for constructing our command string
		#time to know what programmer are we using
		programmer_details=common_func.get_programmer_details(self.global_programmer)
		protocol=programmer_details[0]
		cmd_str.append("avrdude")
		cmd_str.append("-c")
		cmd_str.append(protocol)
		cmd_str.append("-p")
		cmd_str.append(self.global_chipname)
		if len(programmer_details)>1:
			speed=str(self.ui.cbobaudrate.text())
			cmd_str.append("-P")
			cmd_str.append(str(self.ui.cboport.currentText()))
			cmd_str.append("-b")
			cmd_str.append(speed)
		memtype=""
		#okay!we have programmer and parameters,now time to checkwhich memory is to be written
		if self.ui.rdoflash.isChecked():
			memtype="flash"
		if self.ui.rdoeeprom.isChecked():
			memtype="eeprom"
		cmd_str.append("-U")
		cmd_str.append(memtype + ":w:"+str_filename+":i")
		output_str=common_func.run_command_capture(cmd_str,True,path_wd)
		self.ui.txtterminal.setText(output_str)
		output_msg=common_func.process_msg(output_str)	
		QtGui.QMessageBox.critical(self,"Message",output_msg)
		
	
	def showaboutbox(self):
                
		self.aboutdialog=aboutbox()
		self.aboutdialog.show()
		
	def bttnterminal_clk(self):
		if self.ui.rdoprgfolder.isChecked()==True:
			if(common_func.IsWin()==True):
				os.system('cmd')
			elif(common_func.IsLinux()==True):
				os.system('gnome-terminal')
		if self.ui.rdohexfolder.isChecked()==True:
			hex_path=str(self.ui.txtfilename.text())
			if not hex_path:
				QtGui.QMessageBox.critical(self,'Error','No file has been selected.')
			else:    
                                common_func.open_terminal_hex_dir(str(hex_path))
				
	#File browser
	def bttnbrowse_clk(self):
		ofd_handle=QtGui.QFileDialog(self)
		ofd_handle.setFilter('Hex files(*.hex)')
		self.filename = ofd_handle.getOpenFileName(self,"","", "Hex files (*.hex);;Bin Files(*.bin);;EEPROM files(*.eep);;All Files(*.*)")
		if os.path.isfile(self.filename):
			self.ui.txtfilename.setText(self.filename)	
	#def bttnprgsettings_clk(self):
	#	ret_text=common_func.run_command_capture(['avrdude','-c','stk500','-p','m2560','-P','/dev/ttyACM0','-b','115200'])
	#	self.ui.txtterminal.setText(ret_text)
	
	def gpcschip_clk(self):
		if self.is_arduino_board==True:
			return
		programmer_details=common_func.get_programmer_details(self.global_programmer)
		protocol=programmer_details[0]
		cmd_str="avrdude -c "+protocol+" -p m8"
		if len(programmer_details)>1:
			speed=programmer_details[1]
			cmd_str=cmd_str+" -P "+str(self.ui.cboport.currentText())+" -b " + speed
		mcu_str=avrdude.get_mcu(cmd_str)
		output_msg=common_func.process_msg(mcu_str)
		if len(output_msg)>0:
			QtGui.QMessageBox.critical(self,'Error',output_msg)
			return None
		self.ui.gpcs_chip.setText(self.format_chipname(mcu_str))
		self.global_chipname=mcu_str
		
    #code for menu actions 
    #programmer selection
	def select_programmer(self,board_name,is_arduino=False):
		print board_name
		print common_func.set_config("programmer_board",board_name)
		programmer_details=common_func.get_programmer_details(board_name)
		if len(programmer_details)>1:
			self.ui.cbobaudrate.setText(programmer_details[1])
		if is_arduino==True:
			self.is_arduino_board=True
			self.global_programmer=board_name
			self.global_chipname=arduino_handler.get_chipname(board_name)
			print self.global_chipname
		else:
			self.is_arduino_board=False
			self.global_programmer=board_name
			self.global_chipname=""
		self.ui.gpcs_chip.setText(self.format_chipname(self.global_chipname))
		self.update_programmer_name()
	def format_chipname(self,chipname):
		if len(chipname)==0:
			return ""
		chip_list=list(chipname)
		chip_list[0]="A"
		chip_list[1]="T"
		return ''.join(chip_list)
		
if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = mainform()
	myapp.show()
	sys.exit(app.exec_())

