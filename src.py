# -*- coding: utf-8 -*-
import vk_api
import json
import requests
from lxml import html
from login import *


def write_msg(user_id, s):
    vk.method('messages.send', {'user_id': user_id, 'message': s})


def is_user_memb(user_id):
    groups = vk.method('groups.getMembers', {"group_id": group_id})
    if int(user_id) in groups['items']:
        return True
    else:
        return False


def get_GoogleInfo(as_q="Python", num = "3"):
    url = "https://www.google.com/search"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
    dat = dict(hl="ru", as_qdr="all", as_occt="any", safe="images", as_q=as_q, num=str(num))
    res = requests.get(url, params=dat, headers=headers)
    tsiu = []
    tm_dct = {}
    tree = html.fromstring(res.content.decode())
    tm_dct['url'] = tree.xpath('//h3[@class = "r"]/a/@href')
    tm_dct['title'] = tree.xpath('//h3[@class = "r"]/a/text()')
    tm_dct['short_info'] = tree.xpath('//span[@class = "st"]/text()')
    tsiu.append(tm_dct.copy())
    return tsiu


def get_GooglePicture(as_q="Python"):
    url = "https://www.google.ru/search"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
    dat = dict(as_st="y", tbm="isch", as_occt="any", safe="images", as_q=as_q, num="3")
    res = requests.get(url, params=dat, headers=headers)

    tree = html.fromstring(res.content.decode())
    f1 = tree.xpath('//div[@class = "rg_meta"]/text()')
    img = []
    for i in f1[:3]:
        img.append(json.loads(i)["ou"])
    return img


def send_photo(photo_name, user_id=my_id):
    photo_name = ["D:\MyFile\\3.jpg", "D:\LIRA\A9DKV_S0_X8.jpg", ]
    photos = upload.photo_messages(photo_name)
    for upl in photos:
        vk.method('messages.send', {'user_id': user_id, 'attachment': "photo{}_{}".format(upl['owner_id'], upl['id'])})


#if __name__=="__main__":
vk = vk_api.VkApi(token=token)
vk.auth()
upload = vk_api.VkUpload(vk)

