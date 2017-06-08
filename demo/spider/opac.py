
import urllib.request
import os
import time
import requests
import re
from bs4 import BeautifulSoup
import  pymysql
import  pymysql.cursors

# 打开数据库连接
db = pymysql.connect("localhost","root","root","exe" )

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute() 方法执行 SQL，如果表存在则删除
cursor.execute("DROP TABLE IF EXISTS exe")

# 使用预处理语句创建表
sql_creat = """CREATE TABLE EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,
         SEX CHAR(1),
         INCOME FLOAT )"""
cursor.execute(sql_creat)

# 关闭数据库连接

def open_url(url):
    # 根据当前URL创建请求包
    req = urllib.request.Request(url)
    # 添加头信息，伪装成浏览器访问
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36')
    # 发起请求
    response = urllib.request.urlopen(req)
    # 返回请求到的HTML信息
    return response.read()


url = 'http://202.119.210.3:8080/opac/item.php?marc_no=0000435712'
html = open_url(url).decode('utf-8')
soup = BeautifulSoup(html)
tt = soup.find_all('dl')
result = {}
data = {}
data['type'] = re.findall('文献类型：(.*)浏览', html)
for ii in tt:
    result[ii.find('dt').text] = ii.find('dd').text

data['title'] = result.get('题名/责任者:')
data['publish'] = result.get('出版发行项:')
data['title1'] = result.get('其它题名:')
data['title2'] = result.get('并列正题名:')

data['flh'] = result.get('中图法分类号:')
data['page'] = result.get('载体形态项:')
data['add'] = result.get('责任者附注:')
data['subject'] = result.get('学科主题:')
data['abstract'] = result.get('豆瓣简介:')

#
# print(data)
# print(result)
# exit()

sql = 'insert into `urls`(`title`,`title1`,`title2`,`flh`,`publish`,`subject`,`page`,`type`,`add`,`abstract`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
cursor.execute(sql, data.values())

db.close()
print(result)
exit()

