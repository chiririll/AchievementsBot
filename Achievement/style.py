from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont


class AchievementStyle:

    def __init__(self, size: tuple, icon_size: tuple, font: str, **params):
        """
        Class for creating different achievements styles
        :param size: Size of achievement
        :param icon_size: Size of achievement's icon
        :param font: Font filepath, should be str
        :param params: Other achievement's params

        Common:
        :key text_color: Color of text, should be PIL.ImageColor
        :key use_copyright: Use copyright, should be boolean

        Message:
        :key message: Message "Achievement unlocked" or other, should be str
        :key msg_size: Max font size of message, should be int
        :key msg_pos: Position of message (top_right, bottom_left), should be tuple

        Icon:
        :key img_pos: Position for icon, should be tuple
        :key img_shape: Shape of icon, should be str

        Background:
        :key bg_image: Background image filepath, should be str
        :key bg_color: Background color, should be PIL.ImageColor

        Name:
        :key name_size: Max font size of name, should be int
        :key name_pos: Static position of name (top_right, bottom_left), should be tuple

        Description:
        :key desc_size: Max font size of description, should be int
        :key desc_pos: Position of description lines (top_right, bottom_left), should be tuple
        """

        self.size = size
        self.icon_size = icon_size
        self.font = font
        self.params = params

        self._check_params()

    # Checking params
    def _check_params(self):
        # Default values
        values = {
            'use_copyright': True,
            'text_color': ImageColor.getrgb("#FFFFFF"),
            'img_shape': 'square',
            'bg_color': ImageColor.getrgb("#000000"),
            'desc_size': 26
        }
        # Setting default values
        for param, val in values.items():
            if param not in self.params.keys():
                self.params[param] = val

    def _get_font(self, target, minor=0):
        targets = {
            'msg': self.params['msg_size'],
            'name': self.params['name_size'],
            'desc': self.params['desc_size']
        }
        return ImageFont.truetype(self.font, targets[target] - minor)

    def _draw_text(self, drawer, text, pos, font_code):
        width = pos[1][0] - pos[0][0]
        height = pos[1][1] - pos[0][1]

        # Fitting image to size
        minor = 0
        size = drawer.textsize(text, self._get_font(font_code, minor))
        while size[0] > width or size[1] > height:
            minor += 1

        # Drawing
        draw_pos = (
            pos[0][0] + (width - size[0]) // 2,
            pos[0][1] + (height - size[1]) // 2
        )
        drawer.text(draw_pos, text, font=self._get_font(font_code), fill=self.params['text_color'])

    def generate(self, name: str, icon: Image = None, description: str = None):
        image = Image.new("RGB", self.size, self.params['bg_color'])
        drawer = ImageDraw.Draw(image)

        # Adding icon
        if not icon:
            self.params['img_shape'] = None

        if self.params['img_shape'] == 'square':
            image.paste(icon.resize(self.icon_size))
        elif self.params['img_shape'] == 'circle':
            mask = Image.new("L", self.icon_size, 0)
            # Mask drawer
            md = ImageDraw.Draw(mask)
            md.ellipse(((5, 5), (self.icon_size[0] - 5, self.icon_size[1] - 5)), fill=255)
            # Blur
            mask = mask.filter(ImageFilter.GaussianBlur(3))
            image.paste(icon.resize(self.icon_size), self.params['img_pos'], mask)

        # Adding message
        self._draw_text(drawer, self.params['message'], self.params['msg_pos'], 'msg')

        # Adding name
        self._draw_text(drawer, f"«{name}»", self.params['name_pos'], 'name')

        # TODO: Add description

        # Adding copyright
        if self.params['use_copyright']:
            text = "vk.com/achievebot"
            font = ImageFont.truetype("Fonts/FlowExt-Bold.otf", 14)
            size = drawer.textsize(text, font)
            pos = (self.size[0] - size[0], self.size[1] - size[1])
            drawer.text(pos, text, font=font, fill=self.params['text_color'])

        return image
