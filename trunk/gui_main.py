#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       gui_main.py
#       
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>

"""
Module implementing gui_main.
"""

from PyQt4.QtGui import QMainWindow,QDialog
from PyQt4.QtCore import pyqtSignature
import PyQt4
from ui.Ui_main import Ui_MainWindow
from ui.dialog_newmission import Ui_dialog_NewMission
import subprocess,sys
import threading
import time

class GuiMain(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent = None):
        """
        Constructor
        """
        self.new_mission = GuiNewMissionDialog()
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
    
    @pyqtSignature("")
    def on_startDaemon_clicked(self):
        """
        Start daemon
        """
        if self.startDaemon.text() == u'开启Daemon':
            self.p = subprocess.Popen('./daemon.py')
            self.startDaemon.setText(u'关闭Daemon')
        else:
            self.p.terminate()
            self.startDaemon.setText(u'开启Daemon')

    def on_newMission_clicked(self):
        """
        Start a new mission, show the newmission dialog box.
        """
        self.new_mission.setVisible(True)

class GuiNewMissionDialog(QDialog, Ui_dialog_NewMission):
    """
    A dialog box, to read url
    """
    global client_subprocess,cv
    
    def __init__(self, parent = None):
        """
        Constructor
        Arguments:
        - `self`:
        - `parent`:
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.clients = []

    def on_buttonBox_NewMission_accepted(self):
        """
        Url confirm. start client.
        """
        subp = subprocess.Popen(('./client.py',self.lineEdit_url.text()),stdout=subprocess.PIPE)
        cv.acquire()
        client_subprocess.append(subp) # todo
        cv.release()
        ui.tableWidget.insertRow(0)
        thread_RefreshGui_instance = Thread_RefreshGui(subp)
        thread_RefreshGui_instance.start()

class Thread_RefreshGui(threading.Thread):
    """
    Thread of refreshing GUI, listen the output of the CLI command.
    """
    
    def __init__(self,client ):
        """Constructor
        """
        threading.Thread.__init__(self)
        self.client = client

    def run(self):
        """the run method of Thread_RefreshGui class.
        """
        while self.client.poll() == None:
            data = self.client.stdout.readline()
            print data
            if data.startswith('Info'):
                data_list = data.split(': ')
                getattr(self,data_list[1]+'_parser')(data_list)
            # cv.acquire()
            # client_output_list = []
            # client_output_list = [i.stdout.readline() for i in client_subprocess] # todo
            # for i in client_subprocess:
            #     data = i.stdout.readline()
            #     while data:
            #         client_output_list.append([])
            #         client_output_list[i].append(data)
            #         data = i.stdout.readline()
            # cv.release()
            # for i in client_output_list:
            #     print i
            #     for j in i:
            #         if i.startswith('Info'):
            #             print 'starts with Info'
            #             j_list = j.split(': ')
            #             if j_list[1] == 'File name':
            #                 print 'j_list[1] == File Name'
            #                 item = PyQt4.QtGui.QTableWidgetItem()
            #                 item.setText(j_list[2])
            #                 ui.tableWidget.setItem(0,0,item)
            # time.sleep(1)

    def FileName_parser(self,list):
        """
        parser of FileName
        Arguments:
        - `list`:
        """
        item = PyQt4.QtGui.QTableWidgetItem()
        item.setText(list[2])
        ui.tableWidget.setItem(0,0,item)
            
    def FileSize_parser(self,list):
        """
        parser of FileSize
        Arguments:
        - `self`:
        - `list`:
        """
        item = PyQt4.QtGui.QTableWidgetItem()
        item.setText(list[2])
        ui.tableWidget.setItem(0,1,item)


if __name__ == "__main__":
    global cv
    client_subprocess = []
    cv = threading.Condition()

    app = PyQt4.QtGui.QApplication(sys.argv)
    ui = GuiMain()
    ui.show()
    sys.exit(app.exec_())
