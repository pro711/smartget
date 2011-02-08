#!/usr/bin/python

# run server, a file named source will be read and sent to client
source = 'source'

import socket
import os
from download import MyURLopener
import threading

def thread_send():
    """
    thread of the sending

    """
    global fifo, lock
    global c
    global finished

    while finished == 0:
        lock.acquire()
        tosend = fifo[:16384]
        fifo = fifo[16384:]
        lock.release()
        c.send(tosend)
    lock.acquire()
    c.send(fifo)
    lock.release()
    
    
def main():
    global fifo, lock
    global c
    global finished
    
    s = socket.socket()
    host = socket.gethostname()
    port = 1234
    s.bind((host,port))
    s.listen(5)
    
    # fp = open(source,'rb')
    # file = fp.read()
    # fp.close()
    while True:
        c,addr=s.accept()
        print 'Got connection from',addr
        
        request_list = c.recv(1024).split('\n')
        print 'Got request:\nURL:'+request_list[0]+'\nStart:'+request_list[1]+'\nEnd:'+request_list[2]
        
        opener = MyURLopener()
        opener.openurl(request_list[0],request_list[1],request_list[2])
        
        finished = 0
        lock = threading.Lock()
        

        data = opener.sock.read(16384)
        fifo = ''
        thread_send_instance = threading.Thread(target=thread_send)
        thread_send_instance.start()
        while data:
            lock.acquire()
            fifo += data
            lock.release()
            data = opener.sock.read(16384)
        finished = 1
        thread_send_instance.join()
        c.close()

if __name__ == '__main__':
    main()
