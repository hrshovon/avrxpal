import os
import sys
from PyQt4 import QtCore, QtGui
from aboutdialog import Ui_frmabout
import common_func
#import ext_stuffs
#import avrdude
class aboutbox(QtGui.QMainWindow):
	def __init__(self, parent=None):
		QtGui.QWidget.__init__(self, parent)
		self.ui = Ui_frmabout()
		self.ui.setupUi(self)		


