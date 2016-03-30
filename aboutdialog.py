# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aboutdialog.ui'
#
# Created: Fri Oct 31 02:15:11 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_frmabout(object):
    def setupUi(self, frmabout):
        frmabout.setObjectName(_fromUtf8("frmabout"))
        frmabout.resize(589, 251)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../../../home/shovon/Desktop/python stuffs/gui/SMD-64-pin.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        frmabout.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(frmabout)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(280, 10, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(280, 70, 101, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 241, 201))
        self.label_3.setText(_fromUtf8(""))
        self.label_3.setPixmap(QtGui.QPixmap(_fromUtf8("../../../../home/shovon/Desktop/python stuffs/gui/SMD-64-pin.ico")))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(280, 100, 91, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(280, 120, 291, 51))
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        frmabout.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(frmabout)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        frmabout.setStatusBar(self.statusbar)

        self.retranslateUi(frmabout)
        QtCore.QMetaObject.connectSlotsByName(frmabout)

    def retranslateUi(self, frmabout):
        frmabout.setWindowTitle(_translate("frmabout", "About", None))
        self.label.setText(_translate("frmabout", "AVRxpal", None))
        self.label_2.setText(_translate("frmabout", "CEMSTech Inc.", None))
        self.label_4.setText(_translate("frmabout", "Version 1.0.0", None))
        self.label_5.setText(_translate("frmabout", "A cross platform avrdude GUi.\n"
"It\'s open source.you are free to \n"
"develop it more.\n"
"", None))

