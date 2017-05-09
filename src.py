# -*- coding: utf-8 -*-
import vk_api
import json
import requests
import os
import re
import time
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
    photo_mas = []
    for i, img in enumerate(photo_name):
        upl = requests.get(img)
        new_name = str(i)+os.path.splitext(img)[1]
        new_name = re.findall(r"([\d]?\.(jpeg|png|jpg|gif))", new_name)[0][0]###################################################################
        with open(new_name, "wb") as fl:
            fl.write(upl.content)
        try:
            upld = upload.photo_messages(new_name)[0]
        except vk_api.exceptions.ApiError:
            pass
        else:
            os.remove(new_name)
            photo_mas.append("photo{}_{}".format(upld['owner_id'], upld['id']))
    vk.method('messages.send', {'user_id': user_id, 'attachment': ",".join(photo_mas)})


def run():
    values = {'out': 0, 'count': 1, 'time_offset': 30}
    while True:
        response = vk.method('messages.get', values)
        if response['items']:
            values['last_message_id'] = response['items'][0]['id']
            print(response['items'])
        for item in response['items']:
            info = get_GoogleInfo(item["body"])[0]
            img = get_GooglePicture(item["body"])
            for i in range(len(info)-1):
                write_msg(item['user_id'], "*{} / {} / {}".format(info['title'][i], info['short_info'][i], info['url'][i]))
            send_photo(img, item['user_id'])
        time.sleep(0.5)

if __name__=="__main__":
    vk = vk_api.VkApi(token=token)
    vk.auth()
    upload = vk_api.VkUpload(vk)
    run()





