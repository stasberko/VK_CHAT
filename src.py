# -*- coding: utf-8 -*-
import vk_api
import time
from bs4 import BeautifulSoup
import requests
from login import *

def write_msg(user_id, s):
    vk.method('messages.send', {'user_id': user_id, 'message': s})


def is_user_memb(user_id):
    groups = vk.method('groups.getMembers', {"group_id": group_id})
    if int(user_id) in groups['items']:
        return True
    else:
        return False

vk = vk_api.VkApi(token=token)
vk.auth()
values = {'out': 0, 'count': 100, 'time_offset': 0}

text = "Python"
url = "https://www.google.com/search"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
r = requests.get(url, headers = headers)
dat = dict(hl="ru",as_qdr="all",as_occt="any",safe="images",as_q="Python",num="3")
res = requests.get(url, params=dat, headers=headers)


soup = BeautifulSoup(res.text, "lxml")
res_list = soup.findAll('div', {'class': 'g'})

tsiu=[]
tm_dct={}
for i in res_list:
    tm_dct['url'] = i.find('h3', {'class': 'r'}).find("a").get("href")
    tm_dct['title'] = i.find('h3', {'class': 'r'}).find("a").text
    tm_dct['short_info'] = i.find('span', {'class': 'st'}).text
    tsiu.append(tm_dct.copy())

for i in tsiu:
    print(i)
