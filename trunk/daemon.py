#!/usr/bin/python

# run server, a file named source will be read and sent to client
source = 'source'

import socket
import os
from download import MyURLopener
import threading

def thread_send(client,thread_id):
    """
    thread of sending

    """
    global fifo, lock
    global finished

    while finished[thread_id] == 0:
        lock.acquire()
        tosend = fifo[thread_id][:16384]
        fifo[thread_id] = fifo[thread_id][16384:]
        lock.release()
        client.send(tosend)
    lock.acquire()
    client.send(fifo[thread_id])
    fifo[thread_id] = ''
    lock.release()

def thread_accept(c):
    """
    thread of accepting
    """
    global fifo, lock
    global finished

    thread_id = threading._get_ident()

    request_list = c.recv(1024).split('\n')
    print 'Got request:\nURL:'+request_list[0]+'\nStart:'+request_list[1]+'\nEnd:'+request_list[2]
    
    opener = MyURLopener()
    opener.openurl(request_list[0],request_list[1],request_list[2])
    
    finished[thread_id] = 0
    lock = threading.Lock()
    

    data = opener.sock.read(16384)
    fifo[thread_id] = ''
    thread_send_instance = threading.Thread(target=thread_send,args=(c,thread_id))
    thread_send_instance.start()
    while data:
        if not(thread_send_instance.is_alive()):
            break
        lock.acquire()
        fifo[thread_id] += data
        lock.release()
        data = opener.sock.read(16384)
    finished[thread_id] = 1
    thread_send_instance.join()
    c.close()
    
    
def main():
    global fifo, lock
    global finished
    fifo = {}
    finished = {}
    thread_accept_list = []
    
    s = socket.socket()
    host = socket.gethostname()
    port = 1234
    s.bind((host,port))
    s.listen(5)
    
    while True:
        c,addr=s.accept()

        print 'Got connection from',addr
        thread_accept_instance = threading.Thread(target=thread_accept,args=((c,)))
        thread_accept_list.append(thread_accept_instance)
        thread_accept_instance.start()

        
        

if __name__ == '__main__':
    main()
