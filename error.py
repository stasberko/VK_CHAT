# -*- coding: utf-8 -*-
import vk_api
from login import *
def write_msg(user_id, s):
    vk.method('messages.send', {'user_id': user_id, 'message': s})

if __name__ == "__main__":
    vk = vk_api.VkApi(token=token)
    vk.auth()
    upload = vk_api.VkUpload(vk)
    values = {'out': 0, 'count': 10, 'time_offset': 30}
    while True:
        response = vk.method('messages.get', values)
        if response['items']:
            values['last_message_id'] = response['items'][0]['id']
            print(response['items'][0])
            for item in response['items']:
                write_msg(item['user_id'], "Я відпочиваю. Вибачте за тимчасові незручності))")