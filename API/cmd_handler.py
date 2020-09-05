from Achievement import get_google


class CommandHandler:

    def __init__(self, payload):
        """
        Class for handling button actions
        :param payload: Button data
        """

        self.commands = {
            'start': self._start,
            'other_images': self._other_images(),
            'other_styles': self._other_styles(),
            'generate': None
        }

        self.payload = payload
        self.cmd = self.payload['command']

    def handle(self):
        return self.commands[self.cmd]()

    # Commands #
    def _start(self):
        return {'message': 'greeting'}

    def _other_images(self):
        urls = []
        if self.payload['params']['search_request']:
            urls = get_google(self.payload['params']['search_request'], self.payload['params']['search_all'], True)
        else:
            urls = get_google(self.payload['params']['name'], self.payload['params']['search_all'], True)

        keyboard = []
        for i in range(1, 10):
            payload = self.payload
            payload['img_index'] = i
            payload['command'] = 'generate'
            keyboard.append({'label': str(i), 'color': 'normal', 'payload': payload})

        return {'message': 'choose_image', 'img_urls': urls, 'keyboard': keyboard}

    def _other_styles(self):
        keyboard = []
        for i in range(1, 4):
            payload = self.payload
            payload['style'] = i
            payload['command'] = 'generate'
            keyboard.append({'label': str(i), 'color': 'normal', 'payload': payload})

        return {'message': 'choose_image', 'attachments': [], 'keyboard': keyboard}

    def _generate(self):
        pass
