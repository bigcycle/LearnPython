# -*- coding: utf-8 -*-

import urllib2
import re


class QSBK():
    """docstring for QSBK"""
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        self.headers = {'User-Agent': self.user_agent}
        self.enable = False
        self.stories = []

    def getPage(self, pageIndex):
        try:
            request = urllib2.Request("http://www.qiushibaike.com/hot/page/" +
                                      str(self.pageIndex),
                                      headers=self.headers)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')
            return content

        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print "Unable to Connect to QSBK, error: ", e.reason
                return None

    def getPageIterm(self, pageIndex):
        pageContent = self.getPage(pageIndex)

        pattern = re.compile('<div.*?author clearfix.*?<h2>(.*?)' +
                             '</h2>.*?<div class="content">(.*?)' +
                             '</div>(.*?)<div class="' +
                             'stats.*?number">(.*?)</i>',
                             re.S)
        iterms = re.findall(pattern, pageContent)
        pageStories = []
        for iterm in iterms:
            haveImg = re.search("img", iterm[2])
            if not haveImg:
                text = re.sub(r'<br/>', "\n\r", iterm[1])
                pageStories.append([iterm[0], text, iterm[3]])
        return pageStories

    def loadPage(self):
        if self.enable:
            pageStories = self.getPageIterm(self.pageIndex)
            if pageStories:
                self.stories.append(pageStories)
                self.pageIndex += 1

    def getOnePage(self, pageStories, page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == 'Q':
                self.enable = False
                return
            print "Page %d\tAuthor:%s\tGood:%s\n%s" % (
                page, story[0], story[2], story[1])

    def start(self):
        print "Scanning QSBK, Press Enter to load next story, 'Q' to exit"
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOnePage(pageStories, nowPage)
spider = QSBK()
spider.start()
