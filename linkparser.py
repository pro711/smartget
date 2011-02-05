#!/usr/bin/python

from sgmllib import SGMLParser
import htmlentitydefs

class LinkParser(SGMLParser):
    """Link Parser, to parse the given url of a
    html file
    """
    temp = {}
    links = {}

    def reset(self):
        """
        reset function
        Arguments:
        - `self`:
        """
        self.temp={}
        self.links={}
        SGMLParser.reset(self)

    def start_a(self,attrs):
        """
        A method to parse url links
        Arguments:
        - `self`:
        - `attrs`:
        """

        for k,v in attrs:
            if k == 'href':
                self.temp[v] = ''
                
    def handle_data(self,text):
        """
        Data handler, if text is an 'a', copy the text.
        Arguments:
        - `self`:
        - `text`:
        """
        if self.temp:
            for k in self.temp:
                self.links[k] = text
            self.temp = {}
        
