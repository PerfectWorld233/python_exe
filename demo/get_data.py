import pymysql
import requests
import re
from bs4 import BeautifulSoup
baseUrl = "http://opac.cpu.edu.cn/opac/item.php?marc_no=0000150884"
def get_content ():
    url = baseUrl
    lists = []
    html = requests.get(url)
    print(html)
    exit()
    p = re.compile(r'/中图法分类号:<\/dt>(.*)<\/dl>/')
    print(p.findall(html))
    exit()

    m = re.match(r'/中图法分类号:<\/dt>(.*)<\/dl>/', html)
    print(m.string)
    exit()
    soup = BeautifulSoup(html.content, "html.parser")
    print(soup)
    exit()
    items = soup.find("ol", "grid_view").find_all("li")
    for i in items:
        movie = {}
        movie["title"] = i.find("em").text
        movie["link"] = i.find("div","pic").find("a").get("href")
        movie["poster"] = i.find("div","pic").find("a").find('img').get("src")
        movie["name"] = i.find("span", "title").text
        movie["score"] = i.find("span", "rating_num").text
        movie["quote"] = i.find("span", "inq").text if(i.find("span", "inq")) else ""
        lists.append(movie)
    return lists
get_content()