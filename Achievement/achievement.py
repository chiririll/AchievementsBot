from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
from .style import Style


# TODO: Add secret achievements
class Achievement:

    def __init__(self, style: Style, name: str, icon=None, description: str = ""):
        self.__style = style

        # Adding icon
        if icon:
            self.__icon = Image.open(icon)
        else:
            icon = self.__style.get_attachment('unknown.png')
            self.__icon = Image.open(BytesIO(icon) if icon else "Images/unknown.jpg")

        self.__strings = {
            'name': name,
            'description': description
        }

        self.__image = Image.new("RGBA", self.__style.get_size(), self.__style.get_color('_BG'))
        self.__drawer = ImageDraw.Draw(self.__image)

    # TODO: add multiline text for description
    # TODO: add filters
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
                print(f"Error handling layer #{i} \"{layer.get('@type')}\" at style \"{self.__style.get_name()}\": {e}")
                return "error.style.layer"

        return self.__image

    # Drawers #
    # TODO: Make some params (font, font_size) optional
    # TODO: Draw every letter
    # TODO: Add more types of font
    def __draw_text(self, layer):
        box = layer['@box']
        font_data = BytesIO(self.__style.get_attachment(layer['@font']))
        # Replacing special markers & getting language string
        text = self.__style.get_string(layer['@text'], **self.__strings)

        width = abs(box[2] - box[0])
        height = abs(box[3] - box[1])

        # Putting image into box
        font_size = layer['@font_size'] + 1
        font = None
        size = (width + 1, height + 1)

        while (size[0] > width or size[1] > height) and font_size > 0:
            font = ImageFont.truetype(font_data, font_size)
            size = self.__drawer.textsize(
                text=text,
                font=font,
                spacing=layer.get('spacing', 4),
                stroke_width=layer.get('stroke_width', 0),
                direction=layer.get('direction'),
                features=layer.get('features'),
                language=layer.get('language')
            )
            font_size -= 1

        if font_size <= 0:
            raise ValueError("Font size too small!")

        # Anchor point
        xy = (
            box[0] + (width - size[0]) // 2,
            box[1] + (height - size[1]) // 2
        )

        color = self.__style.handle_value(layer.get('@font_color'), default='#ffffff')

        self.__drawer.text(
            xy=xy,
            text=text,
            font=font,
            fill=self.__style.get_color(layer.get('@font_color'), '#ffffff'),
            **self.__clear_layer(layer)
        )

    def __draw_image(self, layer):
        if layer['@src'] == '@icon':
            image = self.__icon
        else:
            image = Image.open(BytesIO(self.__style.get_attachment(layer['@src'])))

        mask = Image.open(BytesIO(self.__style.get_attachment(layer['@mask']))) if '@mask' in layer else None

        if layer.get('@foreground'):
            self.__image.alpha_composite(image)
        else:
            self.__image.paste(image, box=layer.get('@box'), mask=mask)

    def __draw_filter(self, layer):
        filters = {
            'color3dlut': ImageFilter.Color3DLUT,
            'boxblur': ImageFilter.BoxBlur,
            'gaussianblur': ImageFilter.GaussianBlur,
            'unsharpmask': ImageFilter.UnsharpMask,
            'rankfilter': ImageFilter.RankFilter,
            'medianfilter': ImageFilter.MedianFilter,
            'minfilter': ImageFilter.MinFilter,
            'maxfilter': ImageFilter.MaxFilter,
            'modefilter': ImageFilter.ModeFilter
        }
        params = self.__clear_layer(layer)
        for k, v in params.items():
            params[k] = self.__style.handle_value(v, **self.__strings)
        f = filters.get(layer['@name'].lower(), lambda **v: None)(**params)
        if f:
            self.__image = self.__image.filter(f)

    def __draw_other(self, layer):
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
            params[k] = self.__style.handle_value(v, **self.__strings)
        types.get(layer['@type'].lower(), lambda **v: None)(**params)
    # ======= #

    # Utils #
    def __clear_layer(self, layer: dict):
        layer = dict(layer)
        keys = list(layer.keys())
        for k in keys:
            if k[0] == '@':
                del layer[k]
        return layer
    # ===== #
