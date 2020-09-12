from io import BytesIO
from random import randint

import requests
from vk_api import vk_api, ApiError, VkUpload
from os import environ as env
from Achievement import Achievement
from API.Utils import CommandHandler, Response


class VK:

    def __init__(self, request: dict):
        """
        Creates a class for handling vk request
        :param request: Request from vk
        """

        vk = vk_api.VkApi(token=env['VK_TOKEN'])
        self.api = vk.get_api()

        self.request = request

    # Handler
    def handle(self):
        # Request type
        r_type = self.request['type']

        # New message event
        if r_type == 'message_new':
            resp = self._message_new()
            self._send_message(resp)

    # Functions #
    def _upload_photo(self, photo: BytesIO):
        # Uploading achievement
        sender = self.request['object']['message']['peer_id']

        # TODO: Fix
        server_url = self.api.photos.getMessagesUploadServer(peer_id=sender)['upload_url']
        upload_req = requests.post(server_url, files={
            'photo': ('photo', photo, f'image/png')
        }).json()

        photo = self.api.photos.saveMessagesPhoto(**upload_req)[0]

        return 'photo' + str(photo['owner_id']) + '_' + str(photo['id']) + '_' + photo['access_key']

    def _send_message(self, resp: Response):
        params = {
            'random_id': self.request['object']['message']['id'],
            'peer_id': self.request['object']['message']['peer_id'],
        }

        if resp.message != '':
            params['message'] = resp.message

        if resp.keyboard:
            params['keyboard'] = resp.keyboard.get_vk()

        if len(resp.img_urls) > 0 or len(resp.images) > 0:
            params['attachments'] = []

        for img in resp.images:
            params['attachments'].append(self._upload_photo(img))

        for url in resp.img_urls:
            req = requests.get(url)
            params['attachments'].append(self._upload_photo(BytesIO(req.content)))

        self.api.messages.send(**params)
        try:
            pass
        except ApiError:
            print(ApiError)
    # --------- #

    # Events #
    def _message_new(self):
        msg = self.request['object']['message']

        # Reading message
        # self.api.messages.markAsRead(peer_id=msg['peer_id'], message_ids=[msg['id']])

        # Checking commands
        if 'payload' in self.request['object']['message']:
            handler = CommandHandler(self.request['object']['message']['payload'])
            return handler.handle()

        # Checking attachments
        image = None
        for attachment in msg['attachments']:
            if attachment['type'] == 'photo':
                for size in attachment['photo']['sizes']:
                    image = size['url']
                    if size['type'] == 'x':
                        break
                break

        ach = Achievement(msg['text'], image)
        return ach.generate()
