from PIL import Image, ImageColor, ImageDraw, ImageFilter, ImageFont


class AchievementStyle:

    def __init__(self, size: tuple, icon_size: tuple, font: str, **params):
        """
        Class for creating different achievements styles
        :param size: Size of achievement
        :param icon_size: Size of achievement's icon
        :param params: Other achievement's params
        :param font: Font filepath, should be str

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
            'img_shape': 'square',
            'bg_color': ImageColor.getrgb("#000000"),
        }
        # Setting default values
        for param, val in values.items():
            if param not in self.params.keys():
                self.params[param] = val

    def _get_font(self, target, size_k=0):
        targets = {
            'msg': self.params['msg_size'],
            'name': self.params['name_size'],
            'desc': self.params['desc_size']
        }
        return ImageFont.truetype(self.font, targets[target] - size_k, 'utf8')

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
            md.ellipse(((0, 0), self.icon_size), fill=255)
            # Blur
            mask = mask.filter(ImageFilter.GaussianBlur(2))
            image.paste(icon.resize(self.icon_size), self.params['img_pos'], mask)

        # Adding message
        pass

        # Adding name #
        name = f"«{name}»"
        width = self.params['name_pos'][1][0] - self.params['name_pos'][0][0]

        # Fitting image to size
        minor = 0
        while drawer.textsize(name, self._get_font('name', minor)) > width:
            minor += 1
        # TODO: Add height fitting and draw text
        # ----- #

        # Adding description
        pass

        # Adding copyright
        pass

        return image
