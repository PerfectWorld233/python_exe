# pool = Pool(n) #建立进程池，n就是代表了建立几个进程，这个n的设定一般与cpu的核数一样
# pool.map(def,list)#把列表list里面的每一项映射到你所定义的def函数内，有点通过这句话做list各项循环的意味
# pool.close()#关闭进程池，不再接受新的进程
# pool.join()#主进程阻塞等待子进程安全退出，父子进程同步
# 在使用多进程的时候还可以加入异步，这个还没有学习，之后会加入进来，在爬取大量的数据时候或者图片的时候会大大的提高效率。
# http://cuiqingcai.com/category/technique/python
# http://blog.csdn.net/leoe_/article/details/65939264
import json
from multiprocessing import Pool
import requests
from requests.exceptions import RequestException
import re

def get_one_page(url): #判断页面的请求状态来做异常处理
    try:
        response = requests.get(url)
        if response.status_code == 200:#200是请求成功
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?<p class="name">.*?data-val.*?>(.*?)</a>'#正则表达式
                         +'.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(\d+)</i>.*?</dd>',re.S)
    items = re.findall(pattern, html) #返回正则结果
    for item in items:  #对结果进行迭代，修饰
        yield{
            '排名：':item[0],
            '电影：':item[1],
            '主演：':item[2].strip()[3:],
            '上映时间：':item[3].strip()[5:],
            '评分：':item[4]+item[5]
        }
def write_to_file(content): #写入文件“result.txt”中
    with open('result.txt', 'a', encoding='utf-8') as f: #以utf-8的编码写入
        f.write(json.dumps(content, ensure_ascii=False) + "\n") #json序列化默认使用ascii编码，这里禁用ascii
        f.close()

def main(page):
    url = "http://maoyan.com/board/4?offset=" + str(page) #page 为页码数
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)

if __name__ == '__main__':
    '''
    for i in range(10):
        main(i*10)
    '''
    pool = Pool() #建立进程池
    pool.map(main, (i*10 for i in range(10)))#映射到主函数中进行循环