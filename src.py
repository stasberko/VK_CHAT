# -*- coding: utf-8 -*-
import vk_api
import time
import requests
from login import *
group_id = "sb_python"

def write_msg(user_id, s):
    vk.method('messages.send', {'user_id': user_id, 'message': s})


def is_user_memb(user_id):
    groups = vk.method('groups.getMembers', {"group_id": group_id})
    if int(user_id) in groups['items']:
        return True
    else:
        return False

vk = vk_api.VkApi(token='3ad337faa1e045d122b1b42966334f143428bb47267a473bcb44d26a3eb656512f6080da3d03cc8e95fb1')#vk_api.VkApi(login=login, password=password)
vk.auth()
values = {'out': 0, 'count': 100, 'time_offset': 0}

res = is_user_memb(my_id)
print(res)
