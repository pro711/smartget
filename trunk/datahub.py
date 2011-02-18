#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       datahub.py
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
import random
import threading

'''This module implements a data hub for smartget networks.'''

class SmartgetNode:
    ''' A node in Smartget networks. '''
    def __init__ (self, node_id, addr, port, name=''):
        ''' Class initialiser 
        node id:
            0: data hub
            1,2,3...: ordinary nodes
        
        node status:
            0: not available
            1,2,3...: number of availble connections
            -1: zombie
        '''
        self.node_id = node_id
        self.addr = addr
        self.port = port
        self.status = 0
        self.n_connections = 0


class AbstractDataHub:
    ''' Abstract data hub class for Smartget networks. '''
    
    def __init__ (self):
        ''' Class initialiser '''
        pass
    
    def make_node(self, addr, port, name=''):
        pass

class SmartgetDataHub(AbstractDataHub):
    ''' Data hub class for Smartget networks. '''
    def __init__ (self):
        ''' Class initialiser '''
        self.nodes = {}
        self.max_node_id = 0
    
    def make_node(self, addr, port, name=''):
        node = SmartgetNode(self.max_node_id+1, addr, port, name)
        self.max_node_id += 1
        return node
    
    def add_node(self, node):
        if not self.nodes.has_key(node.node_id):
            self.nodes[node.node_id] = node
            return 1
        else:
            sys.stderr.write('Warning: Attempt to add node %d which already exists!' % node.node_id)
            return 0
    
    def rm_node(self, node_id):
        try:
            del self.nodes[node_id]
        except KeyError:
            sys.stderr.write('Warning: Attempt to remove node %d which does not exist!' % node_id)
    
    def get_nodes(self):
        return self.nodes
    
    def get_node_by_id(self, node_id):
        return self.nodes.get(node_id, None)
    
    def get_node_ids_by_status(self, status):
        node_ids = filter(lambda i:self.nodes[i].status == status, self.nodes.keys())
        return node_ids
    
    def get_available_node_ids(self):
        node_ids = filter(lambda i:self.nodes[i].status>0, self.nodes.keys())
        return node_ids
    
    def get_node_ids_by_addr(self, addr):
        node_ids = filter(lambda i:self.nodes[i].addr == addr, self.nodes.keys())
        return node_ids
    
    def get_node_ids_by_addr_port(self, addr, port):
        node_ids = filter(lambda i:self.nodes[i].port == port, 
            filter(lambda i:self.nodes[i].addr == addr, self.nodes.keys()))
        return node_ids
    
    def get_idle_node_ids(self):
        return self.get_node_ids_by_status(0)
    
    def get_n_idle_nodes(self):
        return len(self.get_idle_node_ids)
    
    def get_node_status(self, node_id):
        return self.nodes[node_id].status
    
    def set_node_status(self, node_id, status):
        if self.nodes.has_key(node_id):
            self.nodes[node_id].status = status
            return node_id
        else:
            sys.stderr.write('Warning: Attempt to modify node %d which does not exist!' % node_id)
            return 0
    
    def decrease_node_status(self, node_id, n=1):
        if self.nodes.has_key(node_id):
            self.nodes[node_id].status -= n
            return node_id
        else:
            sys.stderr.write('Warning: Attempt to modify node %d which does not exist!' % node_id)
            return 0
        
    

class SmartgetDataHubDaemon:
    ''' Data hub daemon class for Smartget networks. '''
    def __init__ (self, port):
        ''' Class initialiser '''
        self.dh = SmartgetDataHub()
        self.HOST = ''                 # Symbolic name meaning all available interfaces
        self.PORT = port              # Arbitrary non-privileged port
        self.lock = threading.Lock()
        # initialize logger
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger('smartget.datahubdaemon')
        # request dispatcher
        self.dispatcher = {
            'register':     self.process_node_reg_request,
            'deregister':   self.process_node_rm_request,
            'requestnodes': self.process_req_nodes_request,
            'setstatus':    self.process_set_status_request
        }
    
    def listen(self, s):
        '''Listen for incoming requests.'''
        self.logger.info('Listening on port %d' % self.PORT)
        while True:
            # serve forever
            try:
                conn, addr = s.accept()
                thread_accept_instance = threading.Thread(target=self.thread_accept,args=(conn,addr))
                thread_accept_instance.start()
            except KeyboardInterrupt:
                print 'Interrupted by user.\nExiting...\n'
                break


    def thread_accept(self,conn,addr):
        '''thread of accepting an incoming request.'''
        self.logger.info('Connected by %s:%s' % addr)
        data = conn.recv(1024)
        if not data:
            conn.close()
            return
        self.process_request(conn, addr, data)
        conn.close()
        
        
    def process_request(self, conn, addr, data):
        '''Parse and dispatch requests.'''
        data_list = data.strip().split(None, 1)
        if not data_list:
            self.logger.warning('Empty request content')
            return -1
        if data_list[0].startswith('`'):
            # this is a client command
            command = data_list[0][1:]
            arg = data_list[1] if len(data_list) > 1 else None
            try:
                f = self.dispatcher[command]
            except KeyError, e:
                self.logger.error('Invalid request content/command: %s' % e)
                return -1
            # execute command
            self.lock.acquire()
            f_return= f(conn, addr, arg)
            self.lock.release()
            return f_return
        else:
            return None
    
    def process_node_reg_request(self, conn, addr, arg):
        '''Register a new node on the network.'''
        client_port = int(arg)
        node_ids = self.dh.get_node_ids_by_addr_port(addr[0], client_port)
        if not node_ids:
            node = self.dh.make_node(addr[0], client_port)
            self.dh.add_node(node)
            self.logger.info('Registered new node at %s:%s, ID=%d' % (addr[0], client_port, node.node_id))
            conn.send('200 OK\r\n%d' % node.node_id)
        else:
            self.logger.error('Node already exists %s:%s!' % (addr[0], client_port))
            conn.send('400 BAD REQUEST\r\nNode already exists!')
    
    def process_node_rm_request(self, conn, addr, arg):
        '''Remove an existing node from the network.'''
        client_port = int(arg)
        node_ids = self.dh.get_node_ids_by_addr_port(addr[0], client_port)
        if not node_ids:
            self.logger.error('Attempt to remove a node which does not exist!')
            conn.send('404 NOT FOUND\r\n')
        else:
            self.dh.rm_node(node_ids[0])
            self.logger.info('Removed node at %s:%s!' % (addr[0], client_port))
            conn.send('200 OK\r\n')
        
    def process_req_nodes_request(self, conn, addr, arg):
        '''Process request to request some available nodes.'''
        n = int(arg.strip().split()[0])
        node_ids = self.dh.get_available_node_ids()
        n = min(n, len(node_ids))   # limit n to number of available nodes
        if n > 0:
            node_ids = random.sample(node_ids, n)
            r = '200 OK\r\n'
            for i in node_ids:
                node = self.dh.get_node_by_id(i)
                self.dh.decrease_node_status(i)
                r += '%s %d\r\n' % (node.addr, node.port)
            conn.send(r)
        else:
            r = '404 NOT FOUND\r\n'
            conn.send(r)
        
    
    def process_set_status_request(self, conn, addr, arg):
        '''Process request to set the status of a node.'''
        node_id, status = arg.strip().split()
        
        if self.dh.set_node_status(int(node_id), int(status)):
            self.logger.info('Node %s status set to %s' % (node_id, status))
            conn.send('200 OK\r\n')
        else:
            self.logger.error('Node does not exist!')
            conn.send('400 BAD REQUEST\r\n')
            
    
    def process_init_download_request(self, conn, addr, request):
        '''Process request to initiate a download.'''
        pass
    
    def process_end_download_request(self, conn, addr, request):
        '''Process request to end a download.'''
        pass
    
    def run(self):
        '''Start data hub daemon.'''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.HOST, self.PORT))
        s.listen(5)
        # start listening for incoming requests
        self.listen(s)
        s.close()
    
    


def main():
    PORT = 20110
    dhd = SmartgetDataHubDaemon(PORT)
    dhd.run()

if __name__ == '__main__':
	main()

