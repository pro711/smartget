#!/usr/bin/python

# run server, a file named source will be read and sent to client
DOWNLOAD_BLOCK_SIZE = 262144

import socket
import os
from download import MyURLopener
import threading
import time

def thread_send(client,thread_id):
    """
    thread of sending

    """
    global fifo, lock, cv
    global finished

    client.setblocking(1)
    while finished[thread_id] == 0:
        lock.acquire()
        try:
            tosend = fifo[thread_id][0]
        except IndexError:
            lock.release()
            cv.acquire()
            cv.wait(0.1)
            cv.release()
            continue
        lock.release()
        try:
            client.send(tosend)
            del(fifo[thread_id][0])
        except socket.error:
            print 'broken pipe'
            del(fifo[thread_id])
            return
    for i in fifo[thread_id]:
        lock.acquire()
        tosend = i
        lock.release()
        try:
            client.send(tosend)
        except socket.error:
            print 'broken pipe'
            break
    del(fifo[thread_id])
    
def thread_accept(c):
    """
    thread of accepting
    """
    global fifo, lock, cv
    global finished

    thread_id = threading._get_ident()

    request_list = c.recv(1024).split('\n')
    print 'Got request:\nURL:'+request_list[0]+'\nStart:'+request_list[1]+'\nEnd:'+request_list[2]
    
    opener = MyURLopener()
    try:
        opener.openurl(request_list[0],request_list[1],request_list[2])
    except IOError:
        return
    
    finished[thread_id] = 0
    lock = threading.Lock()

    data = opener.sock.read(16384)
    fifo[thread_id] = []
    thread_send_instance = threading.Thread(target=thread_send,args=(c,thread_id))
    thread_send_instance.start()
    while data:
        if not(thread_send_instance.is_alive()):
            break
        lock.acquire()
        fifo[thread_id].append(data)
        lock.release()
        data = opener.sock.read(DOWNLOAD_BLOCK_SIZE) # debug
    finished[thread_id] = 1
    thread_send_instance.join()
    c.close()
    
    
def main():
    global fifo, lock, cv
    global finished
    fifo = {}
    finished = {}
    thread_accept_list = []
    
    s = socket.socket()
    host = socket.gethostname()
    port = 1234
    s.bind((host,port))
    s.settimeout(None)
    s.listen(5)
    cv = threading.Condition()
    
    while True:
        c,addr=s.accept()

        print 'Got connection from',addr
        thread_accept_instance = threading.Thread(target=thread_accept,args=((c,)))
        thread_accept_list.append(thread_accept_instance)
        thread_accept_instance.start()

        
        

if __name__ == '__main__':
    socket.setdefaulttimeout(5)
    main()
