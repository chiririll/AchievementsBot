from io import BytesIO
import requests
from lang import lang
from random import randint, choice
from PIL import Image, ImageDraw, ImageColor, ImageFont
from bs4 import BeautifulSoup


# TODO: Add secret achievements
class Achievement:

    def __init__(self, name: str, **params):
        """
        :param name: Name of achievement, should be str
        :param params: Info about achievement

        :key desc: Description of achievement, should be str
        :key image: URL of achievement's icon, should be str
        :key lang: Language of achievement icon, should be str
        :key style: Achievement style, should be int
        :key bg_color: Background color, should be str
        :key text_color: Text color, should be str
        """
        # Saving params
        self.params = params
        del params

        # Name
        self.name = name
        if len(name) > self.get_max('name'):
            self.name = name[:self.get_max('name')]
            # TODO: send message "Bad name"

        # Image
        if 'image' in self.params.keys() and self.params['image']:
            self.image = self.params['image']
            del self.params['image']
        else:
            print("Finding image...", end=' ')
            self.image = self._find_image()
            print("Done!")

        # Description
        if 'desc' in self.params.keys() and len(self.params['desc']) > self.get_max('desc'):
            self.params['desc'] = self.params['desc'][:self.get_max('desc')]
            # TODO: send message "Bad desc"

        # Lang
        if 'lang' in self.params.keys() and self.params['lang'] in lang:
            self.lang = lang[self.params['lang']]
        else:
            self.lang = lang['ru']

        # Image
        self.achievement = None

        # Style
        if 'style' in self.params.keys():
            self._draw(self.params['style'])
        else:
            self._draw(0)

    @staticmethod
    def get_max(key):
        """ Returns max length of name or description """
        max_len = {
            'name': 30,
            'desc': 100
        }
        return max_len[key]

    @staticmethod
    def _get_size(meta_text):
        number = ""
        for symb in meta_text:
            if symb == '×':
                break
            else:
                number += symb
        try:
            return int(number)
        except ValueError:
            return 0

    def _find_image(self):
        url = "https://yandex.ru/images/search?iorient=square&text=" + self.name
        req = requests.get(url)
        if req.status_code != 200:
            return 'Images/unknown.jpg'

        soup = BeautifulSoup(req.text, features="html.parser")

        images = soup.findAll("img", {"class": "serp-item__thumb justifier__thumb"})
        meta = soup.findAll("div", {"class": "serp-item__meta"})

        urls = []

        for i in range(0, len(images)):
            if self._get_size(meta[i].text) >= 250:
                urls.append('https:' + images[i]['src'])
            if len(urls) >= 3:
                return choice(urls)
        if len(urls) > 0:
            return choice(urls)
        else:
            return '%Images/unknown.jpg'

    def _get_color(self, obj_paint):
        if obj_paint in self.params:
            # Checking color
            try:
                return ImageColor.getrgb(self.params[obj_paint])
            except ValueError:
                pass
            # Translating color
            try:
                return ImageColor.getrgb(self.lang['colors'][self.params[obj_paint]])
            except ValueError:
                pass
            except KeyError:
                pass
        if obj_paint == 'bg_color':
            return '#000000'
        else:
            return '#FFFFFF'

    def _draw(self, style: int):
        styles = [
            self._style1
        ]
        # Generate achievement with style
        if 0 <= style < len(styles):
            styles[style]()
        else:
            styles[0]()

    def _style1(self):
        # Creating new image
        achievement = Image.new("RGB", (900, 300), self._get_color('bg_color'))

        # Pasting icon
        icon = None
        if self.image[0] == '%':
            icon = Image.open(self.image[1:])
        else:
            resp = requests.get(self.image)     # Downloading image
            icon = Image.open(BytesIO(resp.content)).resize((300, 300))
        achievement.paste(icon)

        # Creating drawer
        d = ImageDraw.Draw(achievement)

        # Writing message
        font = ImageFont.truetype("Fonts/FlowExt-Bold.otf", 45)
        d.text((406, 0), self.lang['unlocked'], font=font, fill=self._get_color('text_color'))

        # Writing name
        self.name = f"«{self.name}»"
        size = 70
        while d.textsize(self.name, ImageFont.truetype("Fonts/FlowExt-Bold.otf", size))[0] > 550:
            size -= 1
        font = ImageFont.truetype("Fonts/FlowExt-Bold.otf", size)
        pos = (
            300 + (600 - d.textsize(self.name, font)[0]) // 2,
            (300 - d.textsize(self.name, font)[1]) // 2
        )
        d.text(pos, self.name, font=font, fill=self._get_color('text_color'))

        # Copyright
        font = ImageFont.truetype("Fonts/FlowExt-Bold.otf", 14)
        d.text((790, 280), "vk.com/achievebot", font=font, fill=self._get_color('text_color'))

        # Saving
        del d
        self.achievement = BytesIO()
        achievement.save(self.achievement, 'PNG')
        self.achievement.seek(0)

    def get(self):
        return self.achievement
