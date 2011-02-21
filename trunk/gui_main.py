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
CALC_SPEED_PER_X_BLOCK = 10

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

    def FileName_parser(self,list):
        """
        parser of FileName
        Arguments:
        - `list`:
        """
        item = PyQt4.QtGui.QTableWidgetItem()
        item.setText(list[2])
        ui.tableWidget.setItem(0,0,item)

    def BlockSize_parser(self,list):
        """
        parser of BlockSize
        Arguments:
        - `self`:
        - `list`:
        """
        self.block_size = int(list[2])
        self.completed_block = 0
        self.time = time.time()
            
    def FileSize_parser(self,list):
        """
        parser of FileSize
        Arguments:
        - `self`:
        - `list`:
        """
        item = PyQt4.QtGui.QTableWidgetItem()
        self.file_size = list[2].strip()[:-2]
        print self.file_size
        item.setText(self.nomalize_size(self.file_size))
        ui.tableWidget.setItem(0,1,item)

    def Completed_parser(self,list):
        """
        parser of Completed Size
        Arguments:
        - `self`:
        - `list`:
        """
        item = PyQt4.QtGui.QTableWidgetItem()
        item2 = PyQt4.QtGui.QTableWidgetItem()
        item3 = PyQt4.QtGui.QTableWidgetItem()
        completed = list[2].split('/')[0]
        item.setText(self.nomalize_size(completed))
        ui.tableWidget.setItem(0,2,item)
        percentage = float(completed)/float(self.file_size)*100
        item2.setText('%d%%'%percentage)
        ui.tableWidget.setItem(0,3,item2)
        self.completed_block += 1
        if self.completed_block == CALC_SPEED_PER_X_BLOCK:
            new_time = time.time()
            speed = self.block_size * CALC_SPEED_PER_X_BLOCK / (new_time - self.time) / 1024
            item3.setText('%d kB/s'%speed)
            ui.tableWidget.setItem(0,5,item3)
            self.time = new_time
            completed_block = 0
                
    def nomalize_size(self,size):
        """
        transfer kB into MB if necessary
        Arguments:
        - `self`:
        - `size`:
        """
        if size[-2:] == 'kB':
            if len(size[:-2])>4:
                return '%dMB'%(int(size[:-2])/1024)
            else:
                return size
        else:
            if len(size)>4:
                return '%dMB'%(int(size)/1024)
            else:
                return size+'kB'

if __name__ == "__main__":
    global cv
    client_subprocess = []
    cv = threading.Condition()

    app = PyQt4.QtGui.QApplication(sys.argv)
    ui = GuiMain()
    ui.show()
    sys.exit(app.exec_())
