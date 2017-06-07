import requests，pymongo, time
from bs4 import BeautifulSoup
from multiprocessing import Pool
from channel_extact import channel_list
from pages_parsing import get_links_from

client = pymongo.MongoClient('localhost', 27017)
gan_ji = client['ganji']
url_list = gan_ji['url_list']
iterm_info = gan_ji['iterm_info']

db_urls = [iterm['url'] for iterm in url_list.find()]  # 在url_list中找到全部的iterm,iterm['url']是url
index_urls = [iterm['url'] for iterm in iterm_info.find()]
x = set(db_urls)
y = set(index_urls)
rest_of_urls = x - y
if __name__ == '__main__':
    pool = Pool()
    # pool = Pool(processes=6)
    pool.map(get_all_links_from, channel_list.split())  # 参数一是函数，接受参数二