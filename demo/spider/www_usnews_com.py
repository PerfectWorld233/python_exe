
import urllib.request
import json
import os
import time
import requests
import re
from bs4 import BeautifulSoup
import  pymysql
import  pymysql.cursors

# 打开数据库连接
# db = pymysql.connect("114.215.91.48","root","root","news")
db = pymysql.connect("localhost","root","root","news")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# 使用预处理语句创建表
sql_creat = """CREATE TABLE IF NOT EXISTS abroad_school_rank (
         city  text,
         name text,
         country_urlname text,
         url text,
         global_rank  text,
         rank text,
         country_subdivision text,
         score text,
         address_line text,
         country_name text,
         urlname text,
         overall_rank_is_tied text,
         id text,
         rank_is_tied text)
         ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8"""
cursor.execute(sql_creat)
def open_url(url):
    # 根据当前URL创建请求包
    req = urllib.request.Request(url)
    # 添加头信息，伪装成浏览器访问
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                   )
    # req.add_header('content-type',
    #                 'text/html; charset=utf-8',
    #                )
    # req.add_header('accept',
    #                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #                )
    req.add_header('cookie',
                   'ak_bmsc=2F6DE254F852694D07A5F175A9F51DEB17C60B161721000051033A595D8AE33B~plEfZkghrV2o3LK7rX+SrIE8qu0zXzOr7WDuxVB138Mxnl8SC8lx30qUvNaXGxsNhqa/NWnF8JH1T18WnCxRkoiH51ORQr2x9fCitJlfb/mF0o794yA12K0AeUx4wsJpU7B0dF6r7CnY33TJwWlH7J5PydzRtFMUpbXrVOOlTHzOHXLtrTO6ilPWwpI1FbnFptvXAZ8LXRKZaKy/bJ3BsI0rvmXPIJAKedSH8uhebIyBk=; __gads=ID=41a68b89448c64c4:T=1496974187:S=ALNI_MZWvvBm-D-DuUEdwshUbEQ-DVOhwg; bm_sv=CAB323B2A6F801ED9133EF5EB1678567~tMVa8m/FI+8hRQ7vfsbk3mV4qa2kXjWVNxDpXLkhu4FBsvGFNUldr8o/q3J8Ok3EpqwXYD2xJx7Bpu/l+hZ63/P43yukDk/zr7oLZSZpv5BdLHDBStlfwACL5MOj+jpcn84cmrzx2l9tlGg/gjGdz5fNsg2kCVbgFov0an470qc=; __ybotu=j3p7rianzp1rhive0a; __ybotv=1496977735192; s_cc=true; s_sq=%5B%5BB%5D%5D; _ga=GA1.2.950631569.1496974179; _gid=GA1.2.919229669.1496974179; _ceg.s=or9fey; _ceg.u=or9fey; OX_plg=pm; utag_main=v_id:015c8a9cf85b000f09905f3ba36a04072004206a0086e$_sn:2$_ss:0$_st:1496979536277$dc_visit:2$_pn:7%3Bexp-session$ses_id:1496977219995%3Bexp-session$dc_event:6%3Bexp-session$dc_region:us-east-1%3Bexp-session; s_fid=034FADF398765790-098B2CAA51EBD282',
                   )

    # 发起请求
    response = urllib.request.urlopen(req)
    # 返回请求到的HTML信息
    return response.read()

for pp in range (1,1000):
    url = 'https://www.usnews.com/education/best-global-universities/rankings?page='+str(pp)+'&format=json'
    html = open_url(url).decode('utf-8')
    result_j = json.loads(html)
    # "city": "Ann Arbor",
    # "name": "University of Michigan--Ann Arbor",
    # "country_urlname": "united-states",
    # "url": "https://www.usnews.com/education/best-global-universities/university-of-michigan-ann-arbor-170976",
    # "global_rank": 17,
    # "rank": 17,
    # "country_subdivision": "MI",
    # "score": 83.4,
    # "address_line": "Ann Arbor, MI",
    # "country_name": "United States",
    # "urlname": "university-of-michigan-ann-arbor",
    # "overall_rank_is_tied": true,
    # "id": "170976",
    # "rank_is_tied": true
    for ii in result_j.get('results'):
        # html_d = open_url(ii.get('url')).decode('utf-8')
        # soup_d = BeautifulSoup(html_d)
        # ii['address'] = soup_d.find('div', 'directory-data').text
        # ii['grade'] = soup_d.find('span', 't-large').text
        # for addr in soup_d.find_all('div', 'directory-data'):
        #     aa = addr.text
        # ii['website'] = aa
        # ii['summary_d'] = soup_d.find('div', attrs={'data-test-id', 'summary-blurb'}).text

        sql = "insert into abroad_school_rank VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, tuple(ii.values()))
db.close()
exit()
# html_d = open_url(result.get('results')).decode('utf-8')
# soup_d = BeautifulSoup(html_d)
# result['address'] = soup_d.find('div', 'directory-data').text
# result['grade'] = soup_d.find('span', 't-large').text
# for addr in soup_d.find_all('div', 'directory-data'):
#     aa = addr.text
# result['website'] = aa
# sql = "insert into abroad_school VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)"
# cursor.execute(sql, tuple(result.values()))
# db.close()
result = json.dumps(html)
# result = tuple(result.values())
print(result)
exit()
soup = BeautifulSoup(html)
items = soup.find('div', id='resultsMain').find_all('div', 'sep')
result = {}
for ii in items:
    result['school_name'] = ii.find('a').text
    result['ranking'] = ii.find('span', 'rankscore-bronze').text
    result['global_score'] = ii.find('div', 't-large t-strong t-constricted').text
    result['url_d'] = ii.find('a')['href']

    html_d = open_url(result['url_d']).decode('utf-8')
    soup_d = BeautifulSoup(html_d)
    result['address'] = soup_d.find('div', 'directory-data').text
    result['grade'] = soup_d.find('span', 't-large').text
    for addr in soup_d.find_all('div', 'directory-data'):
        aa = addr.text
    result['website'] = aa
    sql = "insert into abroad_school VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, tuple(result.values()))
db.close()

