# -*- coding: utf-8 -*-

import urllib2
import re
from Tool import Tool


class BDTB:
    """docstring for BDTB"""
    def __init__(self, myurl, seeLZ):
        self.url = myurl
        self.seeLZ = seeLZ
        self.tool = Tool()
        self.file = None
        self.floor = 1

    def getPage(self, pageNum):

        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        headers = {'User-Agent': user_agent}
        url = self.url + '?see_lz='
        url += self.seeLZ + '&pn=' + str(pageNum)
        request = urllib2.Request(url, headers=headers)
        try:
            response = urllib2.urlopen(request)
            return response.read()
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print "Can't connect to BDTB, error:", e.reason
                return None

    def getTile(self, page):
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1).strip()
        else:
            return None

    def getPageNum(self, page):
        pattern = re.compile('<li class="l_reply_num".*?<span.*?' +
                             '/span>.*?<span.*?>(.*?)</span>',
                             re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1)
        else:
            return None

    def getContent(self, page):
        pattern = re.compile('<div id="post_content.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            content = "\n" + self.tool.replace(item) + "\n"
            contents.append(content)
        return contents

    def setFileTitle(self, title):
        if title is not None:
            self.file = open(self.tool.replace(title) + ".txt", "w+")
        else:
            self.file = open("BDTB.txt", "w+")

    def writeData(self, contents):
        for item in contents:
            floorLine = "\n" + "Floor " + str(self.floor) + "-----------------"
            floorLine += "----------------------------------------------------"
            floorLine += "--------------------------\n"
            self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    def start(self):
        page = self.getPage(1)
        title = self.getTile(page)
        pageNum = int(self.getPageNum(page))
        self.setFileTitle(title)
        if pageNum is None:
            print "URL invalid, please retry."
            return
        try:
            print "The article has " + str(pageNum) + " Pages in total"
            print "Writing the Page 1."
            self.writeData(self.getContent(page))
            if int(pageNum) > 1:
                for i in range(2, int(pageNum) + 1):
                    print "Writing the Page " + str(i) + "."
                    contents = self.getContent(self.getPage(i))
                    self.writeData(contents)
        except IOError, e:
            print "Exception happened during writing:" + e.message
        finally:
                print "Finished writing."

if __name__ == '__main__':
    myurl = raw_input("Enter the address of the article:\n")
    seeLZ = raw_input("Whether just see LZ, Yes enter '1', NO enter '0'\n")
    bdtb_sp = BDTB(myurl, seeLZ)
    bdtb_sp.start()
