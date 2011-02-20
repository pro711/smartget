# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog_newmission.ui'
#
# Created: Sun Feb 20 12:53:44 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_dialog_NewMission(object):
    def setupUi(self, dialog_NewMission):
        dialog_NewMission.setObjectName("dialog_NewMission")
        dialog_NewMission.resize(528, 99)
        self.gridLayout = QtGui.QGridLayout(dialog_NewMission)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_url = QtGui.QLabel(dialog_NewMission)
        self.label_url.setObjectName("label_url")
        self.verticalLayout.addWidget(self.label_url)
        self.lineEdit_url = QtGui.QLineEdit(dialog_NewMission)
        self.lineEdit_url.setObjectName("lineEdit_url")
        self.verticalLayout.addWidget(self.lineEdit_url)
        self.buttonBox_NewMission = QtGui.QDialogButtonBox(dialog_NewMission)
        self.buttonBox_NewMission.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_NewMission.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox_NewMission.setObjectName("buttonBox_NewMission")
        self.verticalLayout.addWidget(self.buttonBox_NewMission)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(dialog_NewMission)
        QtCore.QObject.connect(self.buttonBox_NewMission, QtCore.SIGNAL("accepted()"), dialog_NewMission.accept)
        QtCore.QObject.connect(self.buttonBox_NewMission, QtCore.SIGNAL("rejected()"), dialog_NewMission.close)
        QtCore.QMetaObject.connectSlotsByName(dialog_NewMission)

    def retranslateUi(self, dialog_NewMission):
        dialog_NewMission.setWindowTitle(QtGui.QApplication.translate("dialog_NewMission", "新任务", None, QtGui.QApplication.UnicodeUTF8))
        self.label_url.setText(QtGui.QApplication.translate("dialog_NewMission", "Url:", None, QtGui.QApplication.UnicodeUTF8))

