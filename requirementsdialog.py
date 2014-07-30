# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'requirementsdialog.ui'
#
# Created: Tue Jul 29 10:28:57 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.1
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Ui_Dialog):
        Ui_Dialog.setObjectName("Dialog")
        Ui_Dialog.resize(400, 265)
        self.listWidget_Requirements = QtGui.QListWidget(Ui_Dialog)
        self.listWidget_Requirements.setGeometry(QtCore.QRect(20, 60, 361, 181))
        self.listWidget_Requirements.setObjectName("listWidget_Requirements")
        self.pushButton_getSelect = QtGui.QPushButton(Ui_Dialog)
        self.pushButton_getSelect.setGeometry(QtCore.QRect(20, 20, 114, 32))
        self.pushButton_getSelect.setObjectName("pushButton_getSelect")

        self.retranslateUi(Ui_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Ui_Dialog)

    def retranslateUi(self, Ui_Dialog):
        Ui_Dialog.setWindowTitle(QtGui.QApplication.translate("Ui_Dialog", "requirementsdialog", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_getSelect.setText(QtGui.QApplication.translate("Ui_Dialog", "Get Selected", None, QtGui.QApplication.UnicodeUTF8))

