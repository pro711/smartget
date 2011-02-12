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

'''This module implements a data hub for smartget networks.'''

class SmartgetNode:
    ''' A node in Smartget networks. '''
    def __init__ (self, node_id, addr, port, name=''):
        ''' Class initialiser 
        node id:
            0: data hub
            1,2,3...: ordinary nodes
        
        node status:
            0: UNINITIALZED
            1: IDLE
            2: BUSY
            9: ZOMBIE
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
    
    def make_node(self, node_id, addr, port, name=''):
        pass

class SmartgetDataHub(AbstractDataHub):
    ''' Data hub class for Smartget networks. '''
    def __init__ (self):
        ''' Class initialiser '''
        self.nodes = {}
        self.max_node_id = 0
    
    def make_node(self, node_id, addr, port, name=''):
        node = SmartgetNode(self.max_node_id+1, add, port, name)
        self.max_node_id += 1
    
    def add_node(self, node):
        if not self.nodes.has_key(node.node_id):
            self.nodes[node.node_id] = node
            return 1
        else:
            sys.stderr.write('Warning: Attempt to add node %d which already exists!' % node.node_id)
            return 0
    
    def rm_node(self, node):
        try:
            del self.nodes[node.node_id]
        except KeyError:
            sys.stderr.write('Warning: Attempt to remove node %d which does not exist!' % node.node_id)
    
    def get_nodes(self):
        return self.nodes
    
    def get_node_by_id(self, node_id):
        return self.nodes[node_id]
    
    def get_node_ids_by_status(self, status):
        node_ids = filter(lambda i:self.nodes[i].status == status, self.nodes.keys())
        return node_ids
    
    def get_node_ids_by_addr(self, addr):
        node_ids = filter(lambda i:self.nodes[i].addr == addr, self.nodes.keys())
        return node_ids
    
    def get_idle_node_ids(self):
        return self.get_node_ids_by_status(0)
    
    def get_n_idle_nodes(self):
        return len(self.get_idle_node_ids)
    
    def get_node_status(self, node_id):
        return self.nodes[node_id].status
    
    def set_node_status(self, node_id, status):
        if self.nodes.has_key(node.node_id):
            self.nodes[node.node_id].status = status
            return 1
        else:
            sys.stderr.write('Warning: Attempt to modify node %d which does not exist!' % node.node_id)
            return 0
    

class SmartgetDataHubDaemon:
    ''' Data hub daemon class for Smartget networks. '''
    def __init__ (self):
        ''' Class initialiser '''
        self.dh = SmartgetDataHub()
    
    def listen(self):
        '''Listen for incoming requests.'''
        pass
    
    def parse_request(self, request):
        '''Parse and dispatch requests.'''
        pass
    
    def process_node_reg_request(self, request):
        '''Register a new node on the network.'''
        pass
    
    def process_node_rm_request(self, request):
        '''Remove an existing node from the network.'''
        pass
    
    def process_init_download_request(self, request):
        '''Process request to initiate a download.'''
        pass
    
    def process_end_download_request(self, request):
        '''Process request to end a download.'''
        pass
    
    def run(self):
        '''Start data hub daemon.'''
        pass

def main():
	return 0

if __name__ == '__main__':
	main()

