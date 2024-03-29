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
import time
#coding changing
reload(sys)
#SQL_RESULT，数据库清洗SQL，还要一个模块未实现
#1.SELECT * FROM company58 WHERE email !='' AND LENGTH(PHONE_NO)==11 AND SUBSTR(PHONE_NO,1,1)=='1'
#2.SELECT * FROM company58 WHERE email =='' AND LENGTH(PHONE_NO)==11 AND SUBSTR(PHONE_NO,1,1)=='1'
#3.SELECT * FROM company58 WHERE  not (LENGTH(PHONE_NO)==11 AND SUBSTR(PHONE_NO,1,1)=='1') and hr!=""

#print sys.getdefaultencoding()
sys.setdefaultencoding("utf-8")
headers = {'User-Agent': '"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:26.0) Gecko/20100101 Firefox/26.0"'}
cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))


#数据库名称及城市名称进行设置
city = "sh"
database="HR_hunter_%s.db"%city
conn = sqlite3.connect(database)
#设置区#

business_list={'zplvyoujiudian':'餐饮','jiazhengbaojiexin':'家政保洁/安保','meirongjianshen':'美容/美发','zpjiudian':'酒店/旅游','zpwentiyingshi':'娱乐/休闲','zpanmo':'保健按摩','zpjianshen':'运动健身','renli':'人事/行政/后勤','siji':'司机','zpguanli':'高级管理','yewu':'销售','kefu':'客服','zpshangwumaoyi':'贸易/采购','chaoshishangye':'超市/百货/零售','zptaobao':'淘宝职位','zpfangchan':'房产中介','shichang':'市场/媒介/公关','zpguanggao':'广告/会展/咨询','zpmeishu':'美术/设计/创意','zpshengchankaifa':'普工/技工','zpshengchan':'生产管理/研发','zpwuliucangchu':'物流/仓储','xiaofeipin':'服装/纺织/食品','zhikonganfang':'质控/安防','zpqiche':'汽车制造/服务','tech':'计算机/互联网/通信','zpjixieyiqi':'电子/电气','zpjixie':'机械/仪器仪表','zpfalvzixun':'法律','zhuanye':'教育培训','fanyizhaopin':'翻译','zpxiezuochuban':'编辑/出版/印刷','zpcaiwushenji':'财务/审计/统计','jinrongtouzi':'金融/银行/证券/投资','zpjinrongbaoxian':'保险','zpyiyuanyiliao':'医院/医疗/护理','zpzhiyao':'制药/生物工程','huanbao':'环保','zpfangchanjianzhu':'建筑','zpwuye':'物业管理','nonglinmuyu':'农/林/牧/渔业','zhaopin':'其他职位'}
city_list = {'bj': '北京', 'sh': '上海', 'gz': '广州', 'sz': '深圳', 'nj': '南京', 'hz': '杭州', 'su': '苏州', 'tj': '天津', 'cq':'重庆', 'cd':'成都', 'wh':'武汉','qd':'青岛','wx':'无锡','dl':'大连'}


def get_company(city ,business ,page):
    #电脑端爬取公司信息
    url = "http://" + city + ".58.com/" + business + "/pn" + str(page) + "/?PGTID=0d30365b-0004-f8b5-cb93-88ed5156515e&ClickID=1"
    req = urllib2.Request(url, headers = headers)
    content = urllib2.urlopen(req, timeout=60).read()
    if isinstance(content, unicode):
        pass
    else:
        content = content.encode('utf-8')
    bsobj = BeautifulSoup(content, "lxml")
    company = bsobj.find_all(["a"], class_="fl")
    for each in company:
        company_name = each.get("title")
        company_url = each.get("href")
        for i in range(2, len(company_url)):
            if company_url[-i] == '/':
                company_id = company_url[-i+1: -1]
                break
        if company_name == None or company_id.isdigit() != True:
            continue


        save_company(city,company_name,company_id,company_url,business,page)
        # print company_url, company_id, company_name, get_info(company_id)


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
        hr=htmlSource.xpath("/html/body/div[1]/div[5]/div/div[2]/dl/dd[1]/p/span[2]")[0].text.encode('raw_unicode_escape')
    except Exception as e:
        print  id
        return ["" ,"" ,""]
    try:
        email = htmlSource.xpath("/html/body/div[1]/div[5]/div/div[2]/dl/dd[2]")[0].text
        if email == "\r\n\t\t\t\t\t\t":
            email = ""
    except Exception as e:
        email = ""
    return [phone, hr, email]


def save_company(city, company_name, company_id, company_url, business, page):
    #存数据库
    sql_inq="select count(*) from company58 WHERE COMPANY_ID='" +company_id+"'"
    cu = conn.cursor()
    cu.execute(sql_inq)
    result = cu.fetchone()
    if result[0]  :
        return
    [phone, hr, email]=get_info(company_id)
    sql_insert = "insert into company58(CITY,COMPANY_NAME,COMPANY_ID,COMPANY_URL,BUSINESS,PAGE,HR,PHONE_NO,EMAIL)values("\
                 + "'" + city + "'," + "'" + company_name + "'" + ",'" + str(company_id) + "','" + \
                 company_url + "','" + business_list[business]+ "','" +str(page) + "','"+str(hr)+"','"+phone+"','"+email+"')"
    cu.execute(sql_insert)
    conn.commit()
    time.sleep(1)


def patch():

#补丁
    sql_inq = "select * from company58 where HR='' Order by company_ID"
    cu = conn.cursor()
    cu.execute(sql_inq)
    result = cu.fetchall()
    length = len(result)
    count = 0
    for i in range(length):
        try:
            [phone, hr, email] = get_info(result[i][6])
        except Exception as e :
            print e, result[i][6]
        if hr == "":
            continue
        sql_update = "update company58 set HR= '" + hr + "', PHONE_NO= '" + phone + "', EMAIL= '" + email + "'WHERE COMPANY_ID= '" + result[i][6] + "'"
        cu.execute(sql_update)
        conn.commit()
        count += 1
        print sql_update
        time.sleep(4)
    print "updated:" + str(count) + " all :" + str(length)
    # print result


def patch2():
    sql_inq = "select * from company58 where email like '%	%' "
    cu = conn.cursor()
    cu.execute(sql_inq)
    result = cu.fetchall()
    length = len(result)
    for i in range(length):
        sql_update = "update company58 set EMAIL= '' WHERE COMPANY_ID= '" + result[i][6] + "'"
        cu.execute(sql_update)
        conn.commit()
    print str(length) + "EMAIL have been updated"



for business in business_list:
    for page in range(1, 100):
        try:
            get_company(city, business, page)
        except urllib2.HTTPError, e:
            print('HTTPError: ', e.code, city, business, page,)
        except Exception as e:
            print e, city, business, page,


patch()
patch2()
conn.close()
