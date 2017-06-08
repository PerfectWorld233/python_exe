#!/usr/bin/env python
# encoding: utf-8

import pymysql.cursors

"""
@version: python3.5
@author: zhouhm
@license: Apache Licence
@contact: 58383742@qq.com
@site: http://blog.163.com/chilong_zh/
@software: PyCharm
@file: readmysql.py
@time: 2017/1/13 0013 09:52
"""

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
        # 查询语句
        sql = 'select `urlname`, `urlhref` from `urls` where `id` is not null'
        count = cursor.execute(sql)
        print('数据总行数:', count)

        # 查询所有数据
        # result = cursor.fetchall()
        # print(result)

        # 查询指定个数数据
        result = cursor.fetchmany(size=3)
        print(result)
finally:
    connection.close()