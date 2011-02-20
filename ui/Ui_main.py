# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/ltn/dev/pyqt_designer/main.ui'
#
# Created: Sat Feb 19 21:53:41 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(529, 336)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.newMission = QtGui.QPushButton(self.centralwidget)
        self.newMission.setObjectName("newMission")
        self.horizontalLayout.addWidget(self.newMission)
        self.startDaemon = QtGui.QPushButton(self.centralwidget)
        self.startDaemon.setObjectName("startDaemon")
        self.horizontalLayout.addWidget(self.startDaemon)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget = QtGui.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.verticalLayout.addWidget(self.tableWidget)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 529, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtGui.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.action = QtGui.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtGui.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.menu.addAction(self.action_2)
        self.menu_2.addAction(self.action)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "SmartGet", None, QtGui.QApplication.UnicodeUTF8))
        self.newMission.setText(QtGui.QApplication.translate("MainWindow", "新任务", None, QtGui.QApplication.UnicodeUTF8))
        self.startDaemon.setText(QtGui.QApplication.translate("MainWindow", "开启Daemon", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("MainWindow", "文件名", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("MainWindow", "大小", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("MainWindow", "已完成", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("MainWindow", "%", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("MainWindow", "节点", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(5).setText(QtGui.QApplication.translate("MainWindow", "速度", None, QtGui.QApplication.UnicodeUTF8))
        self.menu.setTitle(QtGui.QApplication.translate("MainWindow", " 文件", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_2.setTitle(QtGui.QApplication.translate("MainWindow", "编辑", None, QtGui.QApplication.UnicodeUTF8))
        self.action.setText(QtGui.QApplication.translate("MainWindow", "首选项", None, QtGui.QApplication.UnicodeUTF8))
        self.action_2.setText(QtGui.QApplication.translate("MainWindow", "添加", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

