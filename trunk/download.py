#!/usr/bin/python

import os, urllib

class MyURLopener(urllib.FancyURLopener):
    """My URL opener, extends FancyURLOpener, to define my own
    user-agents.
    Example:
    newopener = MyURLopener()
    newopener.open(url,start,end)
    newopener.sock.read(length)
    newopener.sock.close()
    """
    
        
    def openurl(self,url,start='0',end='0'):
        """download a url
        
        Arguments:
        - `url`:
        - `start`:
        - `end`:
        """
        self._start = start
        self._end = end
        self.addheader('Range','bytes=%s-' %(self._start) + (self._end!='0' and str(self._end) or ''))
        self.sock = self.open(url)

        
def GetUrlFileSize(url, proxies={}):
    """Get the size of url.
    Arguments:
    - `url`:
    - `proxies = {}`:
    """
    urlHandler = urllib.urlopen( url, proxies=proxies )
    headers = urlHandler.info().headers
    length = 0
    for header in headers:
        if header.find('Length') != -1:
            length = header.split(':')[-1].strip()
            length = int(length)
            return length



if __name__ == '__main__':
    opener = MyURLopener()
    opener.openurl('http://www.xdowns.com/soft/xdowns2009.asp?softid=2767&downid=49&id=2767')
    file = opener.sock.read()
    destination = open('destination','wb')
    destination.write(file)
    destination.close()

