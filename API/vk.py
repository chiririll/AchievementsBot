from random import randint

import requests
import vk_api
from os import environ as env
from achievement import Achievement
from lang import lang, lang_ids


class VK:

    def __init__(self, request: dict):
        vk = vk_api.VkApi(token=env['VK_TOKEN'])
        self.api = vk.get_api()

        self.request = request

    def get_response(self):
        # Request type
        r_type = self.request['type']
        req = self.request


        if r_type == 'confirmation':
            return env['VK_CONFIRM']
        elif req['secret'] != env['VK_SECRET']:
            return 'not vk'

        del req

        if r_type == 'message_new':
            self._message_new()

        return 'ok'

    # Events #
    def _message_new(self):
        msg = self.request['object']['message']
        sender = msg['from_id']

        lcode = 'ru'
        if 0 <= self.request['object']['client_info']['lang_id'] < len(lang_ids):
            lcode = lang_ids[self.request['object']['client_info']['lang_id']]

        # Working with text
        lines = msg['text'].split('\n')

        # Params
        params = {}
        if len(lines) > 1:
            vk_params = lines[len(lines)-1].split(',')
            for param in vk_params:
                try:
                    p_name, p_val = param.split(':', 2)
                except ValueError:
                    continue

                p_name = p_name.strip().lower()
                p_val = p_val.strip()

                if p_name in lang[lcode]['params'].keys():
                    params[lang[lcode]['params'][p_name]] = p_val
                else:
                    params[p_name] = p_val

        # Achievement name
        name = lines[0]
        if len(name) > Achievement.get_max('name'):
            self.api.messages.send(user_id=sender, random_id=randint(-2147483648, 2147483647), message=lang[lcode]['long_name'] + ' ' + str(Achievement.get_max('name')))
            return
        elif name == "":
            self.api.messages.send(user_id=sender, random_id=randint(-2147483648, 2147483647), message=lang[lcode]['unnamed'])
            return

        # Checking attachments
        image = None
        for attachment in msg['attachments']:
            if attachment['type'] == 'photo':
                for size in attachment['photo']['sizes']:
                    image = size['url']
                    if size['type'] == 'x':
                        break
                break

        # Creating achievement
        params['image'] = image
        params['lang'] = lcode
        a = Achievement(name, **params)

        # Uploading achievement
        server_url = self.api.photos.getMessagesUploadServer(peer_id=sender)['upload_url']
        upload_req = requests.post(server_url, files={
            'photo': ('photo.png', a.get(), 'image/png')
        }).json()
        photo = self.api.photos.saveMessagesPhoto(**upload_req)[0]
        photo = 'photo' + str(photo['owner_id']) + '_' + str(photo['id']) + '_' + photo['access_key']

        # Sending achievement to user
        self.api.messages.send(user_id=sender, random_id=randint(-2147483648, 2147483647), attachment=photo)

    # ----- #
