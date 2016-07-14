# -*- coding:utf-8 -*-
import requests
import MySQLdb
import xml
import time
import os
import re

GANJI_URL="http://3g.ganji.com"  #e.g: http://3g.ganji.com/gongsi_40053377
WUBA_URL="http://qy.m.58.com"   #e.g: http://qy.m.58.com/m_detail/38039957906711



if __name__ == "__main__":
    #run
    print "搞个大新闻！"
