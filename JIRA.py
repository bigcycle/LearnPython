# -*- coding: utf-8 -*-

import urllib2
import urllib
import cookielib
import re
from Tool import Tool
import HTMLParser
import os


class JIRA:
    """ docstring for JIRA"""
    def __init__(self):
        self.loginURL = "https://cc-jira.rnd.ki.sw.ericsson.se/login.jsp"
        self.baseURL = "https://cc-jira.rnd.ki.sw.ericsson.se"
        self.cookie = cookielib.CookieJar()
        self.postdata = urllib.urlencode({
            'os_username': 'eyaccui',
            'os_password': 'Summer.2016',
            'os_destination': '',
            'atl_token': '',
            'login': 'Log+In'
        })
        self.handler = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.handler)
        self.tool = Tool()
        self.html_parser = HTMLParser.HTMLParser()

    def getPage(self):
        request = urllib2.Request(url=self.loginURL, data=self.postdata)
        try:
            result = self.opener.open(request)
            return result.read()
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print "Can't connect to JIRA, error:", e.reason
                return None

# Test Purpose
#    def writeData(self, tickets):
#            page = self.opener.open(self.baseURL + tickets[0][1]).read()
#            file = open("test.html", "w+")
#            file.write(page)
    def mkdir(self, path):
        path = path.strip()
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
            return True
        else:
            return False

    def writeContent(self, tickets):

        for ticket in tickets:
            try:
                page = self.opener.open(self.baseURL + ticket[1]).read()
            except urllib2.URLError, e:
                if hasattr(e, "reason"):
                    print "Can't connect to ticket URL, error:", e.reason
                    return None

            pattern1 = re.compile('user-content-block">(.*?)</div>', re.S)
            pattern2 = re.compile('<.*?ser-avatar".*?</span></span>(.*?)</a>' +
                                  '.*?verbose subText.*?<time.*?>(.*?)</time' +
                                  '>.*?action-body flooded">(.*?)</div>',
                                  re.S)
            descripe = re.search(pattern1, page).group(1)
            descripe = self.tool.replace(descripe)
            comments = re.findall(pattern2, page)
            file = open(ticket[0] + ".txt", "w+")
            file.write("Ticket NO: " + ticket[0] + "\n")
            file.write("Title    : " + ticket[2] + "\n")
            file.write("Reporter : " + ticket[3] + "\n")
            file.write("Origin   : " + self.baseURL + ticket[1] + "\n")
            file.write("========================================" +
                       "=====================================\n")
            file.write("<-Description->\n\n" +
                       self.html_parser.unescape(descripe) + "\n")
            for comment in comments:
                comment_parser = self.tool.replace(comment[2])
                file.write("\n--Comments---------------------------" +
                           comment[0].strip() + "    " +
                           self.html_parser.unescape(comment[1]).strip() +
                           "\n\n")
                file.write(self.html_parser.unescape(comment_parser) + "\n")
            file.close()

    def getTicket(self):
        page = self.getPage()
        pattern = re.compile('data-issuekey="(.*?)".*?<a class="issue' +
                             '-link.*?href="(.*?)".*?<td class="summary.*?' +
                             'href.*?>(.*?)</a>.*?<td class' +
                             '="reporter".*?<a.*?>(.*?)</a>.*?class' +
                             '="status.*?<span.*?>(.*?)</span>',
                             re.S)
        tickets = re.findall(pattern, page)
        return tickets

if __name__ == '__main__':
    jira = JIRA()
    jira.writeContent(jira.getTicket())
