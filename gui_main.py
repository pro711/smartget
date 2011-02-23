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
from PyQt4.QtCore import pyqtSignature,Qt
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
        self.tableWidget.setSortingEnabled(True)
        
        self.tableWidget.setColumnWidth(0,250)
        self.tableWidget.setColumnWidth(1,50)
        self.tableWidget.setColumnWidth(2,50)
        self.tableWidget.setColumnWidth(3,35)
        self.tableWidget.setColumnWidth(4,70)
        self.tableWidget.setColumnWidth(5,45)

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

    def closeEvent(self,event):
        """
        Reloaded close Event
        close all the subprocessed we created.
        Arguments:
        - `self`:
        - `event`:
        """
        global client_subprocess,cv
        cv.acquire()
        poll_list = [i.poll() for i in client_subprocess.keys()]
        cv.release()
        if None in poll_list:
            reply = PyQt4.QtGui.QMessageBox.question(self, 'Message', \
                                                     u'还有下载进程运行，确定要退出吗？',\
                                                     PyQt4.QtGui.QMessageBox.Yes, PyQt4.QtGui.QMessageBox.No)
            if reply == PyQt4.QtGui.QMessageBox.Yes:
                [i.terminate() for i in client_subprocess.keys()]
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

class GuiNewMissionDialog(QDialog, Ui_dialog_NewMission):
    """
    A dialog box, to read url
    """
    def __init__(self, parent = None):
        """
        Constructor
        Arguments:
        - `self`:
        - `parent`:
        """
        QDialog.__init__(self, parent)
        self.setupUi(self)

    def on_buttonBox_NewMission_accepted(self):
        """
        Url confirm. start client.
        """
        global client_subprocess,cv,lock_sort
        subp = subprocess.Popen(('./client.py',self.lineEdit_url.text()),stdout=subprocess.PIPE)
        cv.acquire()
        client_subprocess[subp] = '' # todo
        cv.release()
        lock_sort.acquire()
        ui.tableWidget.setSortingEnabled(False)
        
        row_number = ui.tableWidget.rowCount()
        ui.tableWidget.insertRow(row_number)
        thread_RefreshGui_instance = Thread_RefreshGui(subp,row_number)
        thread_RefreshGui_instance.start()

class Thread_RefreshGui(threading.Thread):
    """
    Thread of refreshing GUI, listen the output of the CLI command.
    """
    
    def __init__(self,client,row_number):
        """Constructor
        """
        global lock_sort
        threading.Thread.__init__(self)
        self.client = client
        self.row_number = row_number
        
        self.item_file_name = PyQt4.QtGui.QTableWidgetItem()
        self.item_file_size = PyQt4.QtGui.QTableWidgetItem()
        self.item_completed = PyQt4.QtGui.QTableWidgetItem()
        self.item_percentage = PyQt4.QtGui.QTableWidgetItem()
        self.item_speed = PyQt4.QtGui.QTableWidgetItem()
        self.item_number_of_nodes = PyQt4.QtGui.QTableWidgetItem()

        self.item_file_size.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.item_completed.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.item_percentage.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.item_speed.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.item_number_of_nodes.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)

        self.item_file_name.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
        self.item_file_size.setFlags(Qt.NoItemFlags|Qt.ItemIsEnabled)
        self.item_completed.setFlags(Qt.NoItemFlags|Qt.ItemIsEnabled)
        self.item_percentage.setFlags(Qt.NoItemFlags|Qt.ItemIsEnabled)
        self.item_speed.setFlags(Qt.NoItemFlags|Qt.ItemIsEnabled)
        self.item_number_of_nodes.setFlags(Qt.NoItemFlags|Qt.ItemIsEnabled)
        
        ui.tableWidget.setItem(self.row_number,0,self.item_file_name)
        ui.tableWidget.setItem(self.row_number,1,self.item_file_size)
        ui.tableWidget.setItem(self.row_number,2,self.item_completed)
        ui.tableWidget.setItem(self.row_number,3,self.item_percentage)
        ui.tableWidget.setItem(self.row_number,4,self.item_speed)
        ui.tableWidget.setItem(self.row_number,5,self.item_number_of_nodes)

        ui.tableWidget.setSortingEnabled(True)
        lock_sort.release()
        
    def run(self):
        """the run method of Thread_RefreshGui class.
        """
        while self.client.poll() == None:
            print self.client.poll()
            data = self.client.stdout.readline()
            if not data:
                time.sleep(1)
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
        global cv,client_subprocess
        self.item_file_name.setText(list[2])
        cv.acquire()
        client_subprocess[self.client] = list[2]
        cv.release()

    def BlockSize_parser(self,list):
        """
        parser of BlockSize
        Arguments:
        - `self`:
        - `list`:
        """
        self.block_size = int(list[2])
        self.completed_block = 0
            
    def FileSize_parser(self,list):
        """
        parser of FileSize
        Arguments:
        - `self`:
        - `list`:
        """
        self.file_size = list[2].strip()[:-2]
        print self.file_size
        self.item_file_size.setText(self.nomalize_size(self.file_size))
        self.time = time.time()

    def Completed_parser(self,list):
        """
        parser of Completed Size
        Arguments:
        - `self`:
        - `list`:
        """
        completed = list[2].split('/')[0]
        self.item_completed.setText(self.nomalize_size(completed))
        
        percentage = float(completed)/float(self.file_size)*100
        self.item_percentage.setText('%d%%'%percentage)
        
        self.completed_block += 1
        if self.completed_block == CALC_SPEED_PER_X_BLOCK:
            new_time = time.time()
            speed = self.block_size * CALC_SPEED_PER_X_BLOCK / (new_time - self.time) / 1024
            self.item_speed.setText('%dkB/s'%speed)
            self.time = new_time
            self.completed_block = 0

    def LinkedNodes_parser(self,list):
        """parser of LinkedNodes
        """
        self.item_number_of_nodes.setText(list[2])

    def Finish_parser(self,list):
        """
        parser of Finish and average speed
        Arguments:
        - `self`:
        - `list`:
        """
        avs = list[2][6:] + u'平均'
        self.item_speed.setText(avs)

                
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
    global cv,client_subprocess,lock_sort
    client_subprocess = {}
    cv = threading.Condition()
    lock_sort = threading.Lock()
    app = PyQt4.QtGui.QApplication(sys.argv)
    ui = GuiMain()
    ui.show()
    sys.exit(app.exec_())
