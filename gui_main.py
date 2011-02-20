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
        self.clients.append(subprocess.Popen(('./client.py',self.lineEdit_url.text())))

if __name__ == "__main__":
    app = PyQt4.QtGui.QApplication(sys.argv)
    ui = GuiMain()
    ui.show()
    sys.exit(app.exec_())
