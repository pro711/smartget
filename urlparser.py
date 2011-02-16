#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       urlparser.py
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

import re

class UrlParser():
    """Parse url smartly
    """

    keywords = {'u115':r'u.115.com'
                }
    
    def parse(self,url):
        """parse url into a more useful one
        """
        for k,v in self.keywords.iteritems():
            if re.search(v,url):
                return getattr(self,k+'_parser')(url)
        return (url,url.split('/')[-1])

    def u115_parser(self,url):
        """
        u115 parser
        Arguments:
        - `self`:
        - `url`:
        """
        import urllib
        from linkparser import LinkParser
        data = urllib.urlopen(url).read()
        lp = LinkParser()
        lp.feed(data)
        url = [k for k,v in lp.links.iteritems() if re.search(r'(tel|cnc|bak)',k)]
        filename = urllib.unquote(url[0].split('file=')[-1].split('&')[0])
        
        return url,filename
