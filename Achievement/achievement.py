from PIL import Image, ImageDraw, ImageFont
from io import BytesIO


# TODO: Add secret achievements
class Achievement:

    def __init__(self, style, name: str, icon=None, description: str = ""):
        self.__style = style
        self.__icon = Image.open(icon) if icon else None
        self.__name = name
        self.__description = description

        self.__image = Image.new("RGBA", self.__style.get_size(), self.__style.get_color('_BG'))
        self.__drawer = ImageDraw.Draw(self.__image)

    def check(self):
        # TODO: check params
        pass

    # TODO: @color/%color% in every field
    # TODO: add multiline text for description
    def generate(self):
        handlers = {
            'image': self.__draw_image,
            'text': self.__draw_text,
            'foreground': self.__draw_foreground
        }

        # Drawing layers
        for layer in self.__style.get_layers():
            try:
                layer['@type'] = layer['@type'].lower()
                handlers.get(layer['@type'], self.__draw_other)(layer)
            except Exception as e:
                i = self.__style.get_layers().index(layer)
                print(f"Error handling layer #{i} \"{layer.get('@type')}\" at style \"{self.__style.get_name()}\": {e}")
                return "error.style.layer"

        return self.__image

    # Drawers #
    def __draw_text(self, layer):
        box = layer['@box']
        font_data = BytesIO(self.__style.get_attachment(layer['@font']))
        # Replacing special markers & getting language string
        text = self.__text_markers(self.__style.get_string(layer['@text']))

        width = abs(box[2] - box[0])
        height = abs(box[3] - box[1])

        # Putting image into box
        font_size = layer['@font_size']
        font = None
        size = (width + 1, height + 1)

        while size[0] > width or size[1] > height:
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

        # Anchor point
        xy = (
            box[0] + (width - size[0]) // 2,
            box[1] + (height - size[1]) // 2
        )
        layer['align'] = 'center'
        self.__drawer.text(
            xy=xy,
            text=text,
            font=font,
            fill=self.__style.get_color(layer.get('@font_color'), '#ffffff'),
            **self.__clear_layer(layer)
        )

    def __draw_image(self, layer):
        if layer['@src'] == '%icon%':
            if not self.__icon:
                return
            image = self.__icon
        else:
            image = Image.open(BytesIO(self.__style.get_attachment(layer['@src'])))

        mask = None
        if '@mask' in layer:
            mask = Image.open(BytesIO(self.__style.get_attachment(layer['@mask'])))

        self.__image.paste(image, box=layer.get('@box'), mask=mask)

    def __draw_foreground(self, layer):
        image = Image.open(BytesIO(self.__style.get_attachment(layer['@src'])))
        self.__image.alpha_composite(image)

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
        types.get(layer['@type'], lambda: None)(**self.__clear_layer(layer))
    # ======= #

    # Utils #
    def __text_markers(self, text: str):
        markers = {
            '%name%': self.__name,
            '%description%': self.__description
        }

        for k, v in markers.items():
            text = text.replace(k, v)

        return text

    def __clear_layer(self, layer: dict):
        keys = list(layer.keys())
        for k in keys:
            if k[0] == '@':
                del layer[k]
        return layer
    # ===== #
