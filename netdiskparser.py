#!/usr/bin/python

from linkparser import LinkParser
import re

class NetDiskParser():
    """Net Disk Parser, parse Net Disk Links
    Example:
    ndp = NetDiskParser()
    ndp.feed(HTMLSource,'电信')

    all urls contains '电信' would be available in ndp.filelink
    """
    
    filelink = {}
    
    def feed(self,data,pattern):
        """
        feed url to the NetDiskParser
        Arguments:
        - `self`:
        - `data`: a html data to parse
        - `pattern`: a pattern for regular expression
        """
        lp = LinkParser()
        lp.feed(data)
        self.pattern = pattern
        self.links = lp.links
        self.parse()
    
    def parse(self):
        """
        parse links by checking link features
        Arguments:
        - `self`:
        """
        for k,v in self.links.iteritems():
            if re.search(self.pattern,v):
                self.filelink[k] = v
                

