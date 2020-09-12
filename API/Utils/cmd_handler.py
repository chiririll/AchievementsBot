from Achievement.utils import get_google
from .keyboard import Keyboard
from .api_response import Response


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
        return Response(message="Greeting")

    def _other_images(self):
        if self.payload['params']['search_request']:
            urls = get_google(self.payload['params']['search_request'], self.payload['params']['search_all'], True)
        else:
            urls = get_google(self.payload['params']['name'], self.payload['params']['search_all'], True)

        self.payload['command'] = 'generate'
        keyboard = Keyboard(one_time=True)
        keyboard.add_buttons_range(1, 10, payload=self.payload, index_field="img_index")

        return Response(message="choose_image", img_urls=urls, keyboard=keyboard)

    def _other_styles(self):
        self.payload['command'] = 'generate'
        keyboard = Keyboard(one_time=True)
        keyboard.add_buttons_range(1, 4, payload=self.payload, index_field="style")

        return Response(message="choose_style", keyboard=keyboard)

    def _generate(self):
        # TODO: Generate
        return Response(message="Потом доделаю...")
