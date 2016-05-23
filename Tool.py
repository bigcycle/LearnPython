# -*- coding: utf-8 -*-

import re


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
        pass

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.replaceAmp, "&", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()
