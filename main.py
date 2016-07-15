# -*- coding:utf-8 -*-
import requests
import MySQLdb
import xml
import time
import os
import re
import urllib2
import json
import sys
import sqlite3
import cookielib
from lxml import etree
from bs4 import BeautifulSoup
#coding changing
reload(sys)
#print sys.getdefaultencoding()
sys.setdefaultencoding("utf-8")

GANJI_URL="http://3g.ganji.com"  #e.g: http://3g.ganji.com/gongsi_40053377
WUBA_URL="http://qy.m.58.com"   #e.g: http://qy.m.58.com/m_detail/38039957906711


web_headers = {'User-Agent': '"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0"'}
mobile_headers = {'User-Agent': '"Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"'}
cookie = cookielib.CookieJar()
# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

conn = sqlite3.connect("HR_hunter.db")

def get_company_list():
    homepage_for_SH_url = "http://qy.m.58.com/m_entlist/sh/"
    req_for_cookies = requests.get(homepage_for_SH_url, headers = mobile_headers)
    # print req_for_cookies.text
    req_cookies = req_for_cookies.cookies
    print req_cookies
    for page_num in xrange(2,10):
        print page_num
        url="http://qy.m.58.com/m_entlist/ajax_listinfo/"+str(page_num)
        print url
        req = requests.get(url, headers = mobile_headers, cookies = req_cookies)
        content = req.text
        print content

if __name__ == "__main__":
    #run
    print "搞个大新闻！"
    get_company_list()
