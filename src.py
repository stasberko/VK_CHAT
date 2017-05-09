# -*- coding: utf-8 -*-
import vk_api
import json
import requests
import os
import re
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
    t_dct={}
    tree = html.fromstring(res.content.decode())
    for i in range(int(num)):
        try:
            t_dct[i] = \
                (tree.xpath('//h3[@class = "r"]/a/text()')[i],
                 tree.xpath('//span[@class = "st"]/text()')[i],
                 tree.xpath('//h3[@class = "r"]/a/@href')[i])
        except IndexError:
            pass
    return t_dct


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
        try:
            res = re.search(r"[\d]*[.](jpeg|png|jpg|gif)", new_name)###################################################################
            new_name = res.group(0)
        except AttributeError:
            pass
        else:
            with open(new_name, "wb") as fl:
                fl.write(upl.content)
            try:
                upld = upload.photo_messages(new_name)[0]
            except vk_api.exceptions.ApiError:
                pass
            else:
                os.remove(new_name)
                photo_mas.append("photo{}_{}".format(upld['owner_id'], upld['id']))
    if photo_mas:
        vk.method('messages.send', {'user_id': user_id, 'attachment': ",".join(photo_mas)})
    else:
        write_msg(user_id, "Не вдалося знайти жодного зображення")


def run():
    values = {'out': 0, 'count': 10, 'time_offset': 30}
    while True:
        response = vk.method('messages.get', values)
        if response['items']:
            values['last_message_id'] = response['items'][0]['id']
            print(response['items'][0])
            for item in response['items']:
                if not is_user_memb(item["user_id"]):
                    write_msg(item["user_id"],
                    "Привіт, бот доступний тільки для підписників, спочатку підпишись https://vk.com/ukcht а потім напиши знову)) 😃 Команда UkrChat 🖐🏻")
                else:
                    info = get_GoogleInfo(item["body"])
                    img = get_GooglePicture(item["body"])
                    if info:
                        for i in info:
                            write_msg(item['user_id'], "* {} / {} / {}".format(info[i][0], info[i][1], info[i][2],))
                    else:
                        write_msg(item['user_id'], "Не вдалося знайти інформацію")
                    if img:
                        send_photo(img, item['user_id'])
                    else:
                        write_msg(item['user_id'], "Не вдалося знайти жодного зображення")

if __name__ == "__main__":
    vk = vk_api.VkApi(token=token)
    vk.auth()
    upload = vk_api.VkUpload(vk)
    run()



