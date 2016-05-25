# -*- coding:utf-8 -*-

import urllib2
from Tool import Tool
from bs4 import BeautifulSoup
import requests


class iask:
    """docstring for ClassName"""
    def __init__(self):
        self.currentTime = Tool().getCurrentTime
        self.currentDate = Tool().getCurrentDate
        self.replace = Tool().replace
        self.baseURL = "http://iask.sina.com.cn"
        self.initURL = None
        self.soup = None

    def printf(self, *arg):
        print self.currentTime(),
        for n in arg:
            print n,

    def getPage(self, url):
        basePage = requests.get(url)
        self.soup = BeautifulSoup(basePage.text)

    def getQuestions(self):
        questions = self.soup.select('div.question-title')
        for question in questions:
            page = requests.get(self.baseURL + question.a['href'])
            soup = BeautifulSoup(page.text)
            hotWords = soup.select('div.hot-words')
            for hotWord in hotWords:
                hotWord.decompose()
            title = soup.select('div.question_text')[0].pre.get_text()
            author = soup.select('div.ask_autho')[0].a.string
            print 'question', title, author, question.a['href']
            answer_good = self.getGoodAnswer(soup)
            answer_other = self.getOtherAnswers(soup)
            if answer_good:
                print "good answer", answer_good
            if answer_other:
                print 'other answer', answer_other

    def getGoodAnswer(self, soup):
        if soup.select('div.good_answer'):
            good_answer = soup.select('div.good_answer')[0]
            author = good_answer.a.string
            answer_text = soup.select('div.answer_text')[0].span.pre.string
            return [author, answer_text, 1]
        else:
            return None

    def getOtherAnswers(self, soup):
        if soup.select('div.answer_info'):
            answers = soup.select('div.answer_info')
            other_answers = []
            for answer in answers:
                author = answer.a.string
                answer_text = answer.span.pre.string
                other_answers.append([author, answer_text, 0])
            return other_answers
        else:
            return None

    def main(self):
        # f_handler = open('out.log', 'w')
        # sys.stdout = f_handler
        try:
            with open("page.txt", "r") as page:
                content = page.readline()
        except Exception, e:
            self.printf("No fetching record found, will start from Page 1.\n")
            with open("page.txt", "w") as page:
                pass
            self.initURL = self.baseURL + "/c/74.html"
        else:
            self.initURL = self.baseURL + content
        self.getPage(self.initURL)
        initPage = self.soup.select('div.pages')[0]
        self.printf("Start Page:", initPage.div['currentpage'], "\n")
        self.printf("Spider start moving on pages on IASK.sina.\n")
        total_num = initPage['pagecount']
        self.printf("Number of fetched pages: ", total_num, "\n")
        for x in range(int(initPage.div['currentpage']), int(initPage.div['currentpage'])+1):
            if x != int(initPage.div['currentpage']):
                nextPage = initPage.div
                nextPage = nextPage.previous_sibling.previous_sibling['href']
                self.getPage(self.baseURL + nextPage)
            with open("page.txt", "w") as page:
                page.write(self.soup.select('a.cur')[0]['href'])
            try:
                self.getQuestions()
            except urllib2.URLError, e:
                if hasattr(e, "reason"):
                    self.printf("Failed to fetch page !",
                                x, ", Error:", e.reason, "\n")
            # except Exception, e:
            #     self.printf("Failed to fetch page",
            #                 x, ", Error:", e, "\n")

temp1 = iask()
temp1.main()