# -*- coding:utf-8 -*-
import re
import urllib
from urllib import request
# from pprint import pprint
url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9048'
req = urllib.request.Request(url)
r = urllib.request.urlopen(req).read().decode('utf-8')
stations =re.findall(r'([\u4e00-\u9fa5]+)\|([A-Z]+)',r)    # 匹配中文和对应的英文
stations = dict(stations)     # 转化成字典
# pprint(stations)      # 以列的形式打印出来