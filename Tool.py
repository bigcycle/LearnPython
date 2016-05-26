# -*- coding: utf-8 -*-

import re
import time
import HTMLParser
import sys


class Tool:
    """docstring for ClassName"""
    removeImg = re.compile('<img.*?>| {7}')
    removeAddr = re.compile('<a.*?>|</a>')
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    replaceTD = re.compile('<td>')
    replacePara = re.compile('<p.*?>')
    replaceBR = re.compile('<br><br>|<br>')
    replaceAmp = re.compile('&amp;')
    removeExtraTag = re.compile('<.*?>')

    def __init__(self):
        self.html_parser = HTMLParser.HTMLParser()

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.replaceAmp, "&", x)
        x = re.sub(self.removeExtraTag, "", x)
        x = self.html_parser.unescape(x)
        return x.strip()

    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]',
                             time.localtime(time.time()))

    def getCurrentDate(self):
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))

    def log(file):
        def decorator(func):
            def wrapper(*args, **kw):
                f_handler = open(file, 'a')
                sys.stdout = f_handler
                func(*args, **kw)
                f_handler.close()
            return wrapper
        return decorator

    @log('out.log')
    def printf(self, *arg):
        print self.getCurrentTime(),
        for n in arg:
            print n,
