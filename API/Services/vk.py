import requests
from vk_api import keyboard, vk_api, ApiError
from os import environ as env
from Achievement import Achievement
from API.Utils import CommandHandler


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
            # TODO: Handle resp

    # Functions #
    def _upload_photo(self, photo):
        # Uploading achievement
        sender = self.request['object']['message']['peer_id']

        server_url = self.api.photos.getMessagesUploadServer(peer_id=sender)['upload_url']
        upload_req = requests.post(server_url, files={
            'photo': ('photo.png', photo, 'image/png')
        }).json()
        photo = self.api.photos.saveMessagesPhoto(**upload_req)[0]

        return 'photo' + str(photo['owner_id']) + '_' + str(photo['id']) + '_' + photo['access_key']

    def _make_keyboard(self, kb: list):
        if not self.request['object']['client_info']['inline_keyboard']:
            kb[0]['inline'] = False

        vk_kb = keyboard.VkKeyboard(inline=kb[0]['inline'], one_time=kb[0]['one_time'])
        kb = kb[1:]

        count = 0
        for btn in kb:
            count += 1
            if type(btn) is str and btn == 'nl':
                count = 0
                vk_kb.add_line()

            vk_kb.add_button(btn['label'], btn['color'], payload=btn['payload'])
            if count >= 4:
                count = 0
                vk_kb.add_line()

        return vk_kb

    def _send_message(self, **params):
        params['random_id'] = self.request['object']['message']['id']
        params['peer _id'] = self.request['object']['message']['peer_id']
        try:
            self.api.messages.send(**params)
        except ApiError:
            pass
    # --------- #

    # Events #
    def _message_new(self):
        msg = self.request['object']['message']

        # Reading message
        self.api.messages.markAsRead(peer_id=msg['peer_id'], message_ids=[msg['id']])

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

        ach = Achievement(msg, image)
        return ach.generate()
