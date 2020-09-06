import requests

from API import Response, Keyboard, Button
from .utils import get_google
from .style import AchievementStyle
from lang import lang
from io import BytesIO
from PIL import Image


# TODO: Add secret achievements
class Achievement:

    styles = [
        AchievementStyle(
            (900, 300), (300, 300), 'Styles/0/font.otf',
            message="Новое достижение!", msg_size=45, msg_pos=((310, 10), (890, 100)),
            name_size=70, name_pos=((310, 10), (890, 250))
        ),
        AchievementStyle(
            (900, 300), (300, 300), 'Styles/1/font.otf',
            message="Открыто достижение!", msg_size=50, msg_pos=((310, 10), (890, 100)),
            bg_image=Image.open('Styles/1/bg.png'), fg_image=Image.open('Styles/1/fg.png'),
            name_size=70, name_pos=((310, 100), (890, 220)),
            use_copyright=False
        ),
        AchievementStyle(
            (900, 300), (300, 300), 'Styles/2/font.ttf',
            message="Открыто достижение!", msg_size=50, msg_pos=((310, 10), (890, 100)), msg_color=(144, 66, 178),
            bg_image=Image.open('Styles/1/bg.png'), fg_image=Image.open('Styles/1/fg.png'),
            name_size=70, name_pos=((310, 100), (890, 220))
        )
    ]

    def __init__(self, message: str, img_url: str = None):
        self.lang = lang['ru']

        # Global values
        lines = message.split('\n')

        self.name = lines[0]
        self.icon = self._get_image(img_url)
        self.img_url = img_url
        self.description = ""
        self.params = {}

        # Params
        if len(lines) > 1:
            params = lines[len(lines) - 1].split(',')
            for param in params:
                try:
                    p_name, p_val = param.split(':', 2)
                except ValueError:
                    continue

                p_name = p_name.strip().lower().replace('ё', 'е')
                p_val = p_val.strip().lower().replace('ё', 'е')

                if p_name in self.lang['params'].keys():
                    self.params[self.lang['params'][p_name]] = p_val
                else:
                    self.params[p_name] = p_val

        # Lang
        if 'lang' in self.params.keys() and self.params['lang'] in lang.keys():
            self.lang = lang[self.params['lang']]

        self._check_params()

        # Description
        if len(lines) > 2:
            self.description = ' '.join(lines[1:-1])

    def generate(self):
        # Checking length
        if len(self.name) > self.get_max('name'):
            return {'error': True, 'message': "long_name"}
        if len(self.description) > self.get_max('desc'):
            return {'error': True, 'message': "long_desc"}

        if type(self.params['style']) is int and 0 < self.params['style'] <= len(self.styles):
            image = self.styles[self.params['style']-1].generate(self.name, self.icon, self.description)

            payload = {
                'name': self.name,
                'icon': self.img_url,
                'desc': self.description,
                'params': self.params
            }

            keyboard = Keyboard(inline=True)

            payload['command'] = 'other_styles'
            keyboard.add_button(Button('other_styles', payload=payload))

            payload['command'] = 'other_styles'
            keyboard.add_button(Button('other_images', payload=payload))

            return Response(images=[image], keyboard=keyboard)
        else:
            return Response(message="unknown_style")

    @staticmethod
    def get_max(key):
        """ Returns max length of description's name """
        max_len = {
            'name': 30,
            'desc': 50
        }
        return max_len[key]

    def _check_params(self):
        defaults = {
            'lang': 'ru',
            'style': '0',
            'bg_color': '#000000',
            'text_color': '#FFFFFF',
            'search_request': None,
            'search_all': False
        }
        for k, v in defaults:
            if k not in self.params.keys():
                self.params[k] = v

    def _get_image(self, img_url: str = None):
        # Getting from VK or Telegram
        url = img_url

        # Finding in google
        if not url:
            if self.params['search_request']:
                url = get_google(self.params['search_request'], self.params['search_all'])
            else:
                url = get_google(self.name, self.params['search_all'])

        # Unknown
        if not url:
            return Image.open('Images/unknown.jpg')

        # Downloading image
        resp = requests.get(url)
        return Image.open(BytesIO(resp.content))
