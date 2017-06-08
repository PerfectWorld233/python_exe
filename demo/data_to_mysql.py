#!/usr/bin/env python
# encoding: utf-8

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pymysql.cursors

"""
@version: python3.5
@author: zhouhm
@license: Apache Licence
@contact: 58383742@qq.com
@site: http://blog.163.com/chilong_zh/
@software: PyCharm
@file: wiki.py
@time: 2017/1/13 0013 08:50
"""

# 请求URL并把结果用UTF-8编码
resp = urlopen('https://en.wikipedia.org/wiki/Main_Page').read().decode('utf-8')

# 使用BeautifulSoup来解析
soup = BeautifulSoup(resp, 'html.parser')

# 获取所有已wiki开头的<a>标签的信息
listUrls = soup.findAll('a', href=re.compile('^/wiki/'))

# 输出所有的词条对应的名称和URL
for url in listUrls:
    # 过滤.jpg和.JPG结尾的URL
    if not re.search("\.(jpg|JPG)$", url['href']):
        # 输出URL的文字和对应的链接
        print(url.get_text(), "<---->", "https://en.wikipedia.org" + url['href'])
        # 获取数据库链接
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     db='wikiurl',
                                     charset='utf8mb4'
                                     )

        try:
            # 获取会话指针
            with connection.cursor() as cursor:
                # 创建sql语句
                sql = 'insert into `urls`(`urlname`,`urlhref`) VALUES (%s, %s)'

                # 执行sql语句
                cursor.execute(sql, (url.get_text(), "https://en.wikipedia.org" + url['href']))

                # 提交
                connection.commit()
        finally:
            connection.close()