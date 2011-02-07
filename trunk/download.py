#!/usr/bin/python

import os, urllib

def downloadurl(url):
    """
    Open a URL file and store it on your disk.
    Arguments:
    - `url`: a string of the url to download
    """
    sock = urllib.urlopen(url)
    data = sock.read()
    sock.close()
    return data

if __name__ == '__main__':
    file = downloadurl('http://www.xdowns.com/soft/xdowns2009.asp?softid=2767&downid=49&id=2767')
    destination = open('destination','wb')
    destination.write(file)
    destination.close()

