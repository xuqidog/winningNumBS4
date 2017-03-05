# _*_ coding:utf-8 _*_
# Created 2017/3/5
# @author:xu qi dong
# 获取双色球中奖信息


import re
import urllib2
from bs4 import BeautifulSoup
from mylog import MyLog as mylog
from saveExcel import SaveBallDate


class DoubleColorBallItem(object):
    date = None  # 开奖日期
    order = None  # 当年的顺序
    red1 = None  # 第一个红色球号码
    red2 = None  # 第二个红色球号码
    red3 = None  # 第三个红色球号码
    red4 = None  # 第四个红色球号码
    red5 = None  # 第五个红色球号码
    red6 = None  # 第六个红色球号码
    blue = None  # 蓝球号码
    money = None  # 彩池金额
    firstPrize = None  # 一等奖中奖人数
    secondPrize = None  # 二等奖中奖人数


class GetDoubleColorBallNumber(object):
    #  这个类用于获取双色球中奖号码，返回一个txt文件
    def __init__(self):
        self.urls = []
        self.log = mylog()
        self.getUrls()
        self.items = self.spider(self.urls)
        self.pipelines(self.items)  # 写入txt中
        SaveBallDate(self.items)  # 写入excel中
        self.log.info('save data to excel end...\r\n')

    def getUrls(self):
        # 获取数据来源网页
        URL = r'http://kaijiang.zhcw.com/zhcw/html/ssq/list_2.html'
        htmlContent = self.getResponseContent(URL)
        soup = BeautifulSoup(htmlContent, 'lxml')
        tag = soup.find_all(re.compile('p'))[-1]
        pages = tag.strong.get_text()  # 获取所有的页码
        # for i in xrange(1, int(pages)+1):
        for i in xrange(1, 2):
            url = r'http://kaijiang.zhcw.com/zhcw/html/ssq/list_' + str(i) + '.html'
            self.urls.append(url)
            self.log.info(u'添加URL：%s 到URLS \r\n' %url)

    def spider(self, urls):
        # 解析
        items = []
        for url in urls:
            htmlContent = self.getResponseContent(url)
            soup = BeautifulSoup(htmlContent, 'lxml')
            tags = soup.find_all('tr', attrs={})
            for tag in tags:
                if tag.find('em'):
                    item = DoubleColorBallItem()
                    tagTbs = tag.find_all('td')
                    item.date = tagTbs[0].get_text()
                    item.order = tagTbs[1].get_text()
                    tagEms = tagTbs[2].find_all('em')
                    item.red1 = tagEms[0].get_text()
                    item.red2 = tagEms[1].get_text()
                    item.red3 = tagEms[2].get_text()
                    item.red4 = tagEms[3].get_text()
                    item.red5 = tagEms[4].get_text()
                    item.red6 = tagEms[5].get_text()
                    item.blue = tagEms[6].get_text()
                    item.money = tagTbs[3].find('strong').get_text()
                    item.firstPrize = tagTbs[4].find('strong').get_text()
                    item.secondPrize = tagTbs[5].find('strong').get_text()
                    items.append(item)
                    self.log.info(u'获取日期为<<%s>>的数据成功... ' %item.date)
        return items

    # 输出
    def pipelines(self, items):
        fileName = u'双色球.txt'.encode('utf8')
        with open(fileName, 'w') as fp:
            for item in items:
                fp.write(
                    '%s  %s  \t  %s  %s  %s  %s  %s  %s  %s  \t %s  \t  %s  %s \n' % (
                    item.date.encode('utf8'), item.order.encode('utf8'), item.red1.encode('utf8'), item.red2.encode('utf8'), item.red3.encode('utf8'), item.red4.encode('utf8'), item.red5.encode('utf8'), item.red6.encode('utf8'), item.blue.encode('utf8'), item.money.encode('utf8'), item.firstPrize.encode('utf8'), item.secondPrize.encode('utf8')))
                self.log.info(u'日期为<<%s>>的数据输出成功' %item.date)

    # 获取url内容
    def getResponseContent(self, url):
        try:
            response = urllib2.urlopen(url.encode("utf8"))
        except:
            self.log.error(u'Python 返回URL:%s 数据失败' %url)
        else:
            self.log.info(u'Python 返回URL:%s 数据成功' % url)
            return response.read()


if __name__ == '__main__':
    GET = GetDoubleColorBallNumber()
