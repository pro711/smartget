#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       protocol.py
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

import socket

class SmartGetProtocol():
    """SmartGet protocol To communicate with server
    """
    
    def __init__(self, datahub,port=0):
        """
        Initialize
        Arguments:
        - `datahubn`:
        """
        self._datahub = datahub
        self.port = port

    def connect(self):
        """Connect
        """
        self._datahub_socket = socket.socket()
        self._datahub_socket.connect(self._datahub)

    def deregister(self):
        """Deregister
        
        Arguments:
        - `self`:
        """
        self.connect()
        self._datahub_socket.send('`deregister %d'%self.port)
        datahub_message_list = self._datahub_socket.recv(1024).split('\r\n')
        self._datahub_socket.close()
        if datahub_message_list[0]!='200 OK':
            print 'Deregister error!\n'+datahub_message_list[0]

    def register(self):
        """register the node as a daemon
        
        Arguments:

        """
        self.connect()
        self._datahub_socket.send('`register %d'%self.port)
        datahub_message_list = self._datahub_socket.recv(1024).split('\r\n')
        self._datahub_socket.close()
        if datahub_message_list[0]=='200 OK':
            self.node_id = int(datahub_message_list[1])
            print 'Registered successfully. ID = %d'%self.node_id
            return self.node_id
        else:
            print 'register error! '+ datahub_message_list[1]
            raise RegisterError
    
    def setstatus(self,status):
        """set status of the node
        
        Arguments:
        - `status`:status number
        """
        self.connect()
        self._datahub_socket.send('`setstatus %d %d'%(self.node_id,status))
        datahub_message_list = self._datahub_socket.recv(1024).split('\r\n')
        self._datahub_socket.close()
        if datahub_message_list[0] == '200 OK':
            print 'set status %d'%status
        else:
            print 'set status error!'

    def requestnodes(self,n=1):
        """request nodes, default 1 node.
        Return the list of (addr,port)
        Arguments:
        - `n`:
        """
        node_list = []
        self.connect()
        self._datahub_socket.send('`requestnodes %d' %n)
        datahub_message_list = self._datahub_socket.recv(1024).split('\r\n')
        self._datahub_socket.close()
        if datahub_message_list[0] == '200 OK':
            for i in datahub_message_list[1:]:
                addr,port = i.split(' ')
                print 'Got node at %s, port %s'%(addr,port)
                if n==1:
                    return (addr,int(port))
                else:
                    node_list.append((addr,int(port)))
            return node_list
        else:
            print 'Request nodes error!'

class RegisterError(Exception):
    """Register Error
    """
    pass
    # def __init__(self):
    #     """
        
    #     Arguments:
    #     - `value`:
    #     """
    #     pass
    # def __str__(self):
    #     """
        
    #     Arguments:
    #     - `self`:
    #     """
    #     return

