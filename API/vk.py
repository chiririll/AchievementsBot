from random import randint

import requests
import vk_api
from os import environ as env
from achievement import Achievement
from lang import lang


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

        # Achievement name
        name = msg['text']
        if len(name) > Achievement.get_max('name'):
            self.api.messages.send(user_id=sender, random_id=randint(-2147483648, 2147483647), message=lang['ru']['long_name'] + ' ' + str(Achievement.get_max('name')))
            return
        elif name == "":
            self.api.messages.send(user_id=sender, random_id=randint(-2147483648, 2147483647), message=lang['ru']['unnamed'])
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
        a = Achievement(name, image=image)

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
