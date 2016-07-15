#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Zenine
#!/usr/bin/env python
import urllib2
import sys
import sqlite3
import cookielib
from lxml import etree
from bs4 import BeautifulSoup
#coding changing
reload(sys)
#print sys.getdefaultencoding()
sys.setdefaultencoding("utf-8")

headers = {'User-Agent': '"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0"'}
cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

conn = sqlite3.connect("HR_hunter.db")

def get_info(id):
    #返回手机端信息
    url="http://qy.m.58.com/m_detail/"+str(id)
    req = urllib2.Request(url, headers=headers)
    content = urllib2.urlopen(req, timeout=60).read()
    # if isinstance(content, unicode):
    #     pass
    # else:
    #     content = content.encode('GBK')
    htmlSource = etree.HTML(content)
    #company_name=htmlSource.xpath("/html/body/div[1]/div[3]/h1")[0].text
    try:
        phone=htmlSource.xpath("/html/body/div[1]/div[5]/div/div[2]/dl/dd[1]/p/span[1]")[0].text
    except:
        return ["","",""]
    hr=htmlSource.xpath("/html/body/div[1]/div[5]/div/div[2]/dl/dd[1]/p/span[2]")[0].text
    try:
        email=htmlSource.xpath("/html/body/div[1]/div[5]/div/div[2]/dl/dd[2]")[0].text
    except Exception as e :
        email=""
    return [phone,hr,email]

#电脑端页面获取公司ID
url="http://hz.58.com/zplvyoujiudian/pn2/?PGTID=0d30365b-0004-f8b5-cb93-88ed5156515e&ClickID=1"
req = urllib2.Request(url, headers = headers)
content = urllib2.urlopen(req, timeout=60).read()
# if isinstance(content, unicode):
#     pass
# else:
#     content = content.encode('gb2312')
bsObj = BeautifulSoup(content, "lxml")
company=bsObj.find_all(["a"],class_="fl")
for each in company:
    company_url=each.get("href")
    for i in range(2, len(company_url)):
        if company_url[-i] == '/':
            company_id = company_url[-i: -1]
            break
    company_name=each.get("title")
    print company_url,company_id,company_name.decode("utf-8"),get_info(company_id)
