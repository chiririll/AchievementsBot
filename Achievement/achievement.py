import logging
from typing import Dict, Any

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
from .style import Style


# Enable logging
logging.basicConfig(
    format='%(name)s - %(levelname)s: %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# TODO: Add secret achievements
class Achievement:
    LIMITS = {
        'max_name': 30,
        'max_desc': 60
    }

    def __init__(self, style: Style, name: str, icon=None, description: str = ""):
        self.__style = style

        # Adding icon
        self.__icon = (icon or self.__style.get_file('unknown.png')) or "src/unknown.jpg"
        self.__icon = Image.open(self.__icon)

        self.__strings = {
            'name': name,
            'description': description
        }

        self.__image = Image.new("RGBA", self.__style.get_size(), self.__style.get_color('_BG'))
        self.__drawer = ImageDraw.Draw(self.__image)

    @staticmethod
    def check_values(name: str = '', description: str = '', **kwargs):
        if len(name) > Achievement.LIMITS['max_name']:
            yield "error.achievement.long_name"
        if len(description) > Achievement.LIMITS['max_desc']:
            yield "error.achievement.long_desc"

    @staticmethod
    def parse_message(msg):
        if not msg:
            return "error.null_text"
        msg = msg.split('\n')
        return {
            'name': msg[0],
            'description': msg[1] if len(msg) > 1 else ''
        }

    # TODO: add multiline text for description
    # TODO: add random resource @rand
    def generate(self):
        handlers = {
            'image': self.__draw_image,
            'text': self.__draw_text,
            'filter': self.__draw_filter
        }

        # Drawing layers
        for layer in self.__style.get_layers():
            try:
                handlers.get(layer['@type'].lower(), self.__draw_other)(layer)
            except Exception as e:
                i = self.__style.get_layers().index(layer)
                logging.error(f"Error handling layer #{i} ({layer.get('@type')} at \"{self.__style.get_name()}\"): {e}")
                return "error.style.layer"

        # Returning achievement
        file = BytesIO()
        self.__image.save(file, 'PNG')
        file.seek(0)
        return file

    # Drawers #
    # TODO: Draw every letter
    # TODO: Add more types of font
    def __draw_text(self, layer: Dict[str, Any]):
        box = layer['@box']
        # Replacing special markers & getting language string
        text = self.__style.get_string(layer['@text'], **self.__strings)

        # Loading font (if has)
        font_data = self.__style.get_file(layer.get('@font'), "src/default.ttf")

        # Max size of font
        width = abs(box[2] - box[0])
        height = abs(box[3] - box[1])

        def fit(max_size: tuple):
            return max_size[0] < width and max_size[1] < height

        def get_font(font_size):
            if type(font_data) is BytesIO:
                font_data.seek(0)
            return ImageFont.truetype(font=font_data, size=font_size)

        def get_size(font_size):
            return self.__drawer.textsize(
                text=text,
                font=get_font(font_size),
                spacing=layer.get('spacing', 4),
                stroke_width=layer.get('stroke_width', 0),
                direction=layer.get('direction'),
                features=layer.get('features'),
                language=layer.get('language')
            )

        # Putting image into box
        f_size = layer.get('@font_size', 10)
        while not fit(get_size(f_size)):
            f_size -= 1

        # Anchor point
        size = get_size(f_size)
        xy = (
            box[0] + (width - size[0]) // 2,
            box[1] + (height - size[1]) // 2
        )

        self.__drawer.text(
            xy=xy,
            text=text,
            font=get_font(f_size),
            fill=self.__style.get_resource(layer.get('@font_color'), default='#ffffff'),
            **self.__clear_layer(layer)
        )

    def __draw_image(self, layer: Dict[str, Any]):
        # Opening image or icon
        if layer['@src'] == '@icon':
            image = self.__icon
            box = layer['@box']
            image = image.resize((box[2] - box[0], box[3] - box[1]))
        else:
            image = Image.open(self.__style.get_file(layer['@src']))

        mask = Image.open(self.__style.get_file(layer['@mask'])) if '@mask' in layer else None

        if layer.get('@foreground'):
            self.__image.alpha_composite(image)
        else:
            self.__image.paste(image, box=layer.get('@box'), mask=mask)

    def __draw_filter(self, layer: Dict[str, Any]):
        filters = {
            'Color3DULT': ImageFilter.Color3DLUT,
            'BoxBlur': ImageFilter.BoxBlur,
            'GaussianBlur': ImageFilter.GaussianBlur,
            'UnsharpMask': ImageFilter.UnsharpMask,
            'RankFilter': ImageFilter.RankFilter,
            'MedianFilter': ImageFilter.MedianFilter,
            'MinFilter': ImageFilter.MinFilter,
            'MaxFilter': ImageFilter.MaxFilter,
            'ModeFilter': ImageFilter.ModeFilter
        }
        params = self.__clear_layer(layer)
        for k, v in params.items():
            params[k] = self.__style.get_resource(v, **self.__strings)
        f = filters.get(layer['@name'], lambda **z: None)(**params)
        if f:
            self.__image = self.__image.filter(f)

    def __draw_other(self, layer: Dict[str, Any]):
        types = {
            'arc': self.__drawer.arc,
            'bitmap': self.__drawer.bitmap,
            'chord': self.__drawer.chord,
            'ellipse': self.__drawer.ellipse,
            'line': self.__drawer.line,
            'pieslice': self.__drawer.pieslice,
            'point': self.__drawer.point,
            'polygon': self.__drawer.polygon,
            'regular_polygon': self.__drawer.regular_polygon,
            'rectangle': self.__drawer.rectangle,
            'rounded_rectangle': self.__drawer.rounded_rectangle
        }
        params = self.__clear_layer(layer)
        for k, v in params.items():
            params[k] = self.__style.get_resource(v, **self.__strings)
        types.get(layer['@type'].lower(), lambda **z: None)(**params)

    # ======= #

    # Utils #
    @staticmethod
    def __clear_layer(layer: Dict[str, Any]):
        layer = dict(layer)
        keys = list(layer.keys())
        for k in keys:
            if k[0] == '@':
                del layer[k]
        return layer
    # ===== #
