#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       test_datahub.py
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

import os
import sys
import logging
import socket


HOST = '127.0.0.1'    # The remote host
PORT = 20110          # The same port as used by the server

def test_register():
    print 'Testing register...'
    for i in range(2):
        # register
        for port in range(10001,10010):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            s.send('`register %d' % port)
            data = s.recv(1024)
            s.close()
            print 'Received', repr(data)
        # deregister
        for port in range(10001,10010):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            s.send('`deregister %d' % port)
            data = s.recv(1024)
            s.close()
            print 'Received', repr(data)

def test_set_status():
    print 'Testing setstatus...'
    for port in range(10001,10010):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send('`register %d' % port)
        data = s.recv(1024)
        s.close()
        print 'Received', repr(data)
    
        _id = int(data.split('\r\n')[1])
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send('`setstatus %d 1' % _id)
        data = s.recv(1024)
        s.close()
        print 'Received', repr(data)

    for port in range(10001,10010):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send('`deregister %d' % port)
        data = s.recv(1024)
        s.close()
        print 'Received', repr(data)
            
def test_requestnodes():
    print 'Testing requestnodes...'
    for port in range(10001,10010):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send('`register %d' % port)
        data = s.recv(1024)
        s.close()
        print 'Received', repr(data)

    for i in [1,3,6,8]:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send('`requestnodes %d 0' % i)
        data = s.recv(1024)
        s.close()
        print 'Received', repr(data)



def main():
    test_register()
    
    test_set_status()
    
    test_requestnodes()

if __name__ == '__main__':
	main()

