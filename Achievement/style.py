from PIL import ImageColor, Image


class AchievementStyle:

    def __init__(self, size: tuple, img_size: tuple, **params):
        """
        Class for creating different achievements styles
        :param size: Size of achievement
        :param img_size: Size of achievement's icon
        :param params: Other achievement's params

        Message:
        :key message: Message "Achievement unlocked" or other, should be str
        :key msg_size: Size of message text, should be int
        :key msg_pos: Position of message, should be tuple
        :key msg_center: Dynamic position center. should be tuple

        Icon:
        :key img_pos: Position for icon, should be tuple
        :key img_shape: Shape of icon, should be str

        Background:
        :key bg_image: Background image filepath, should be str
        :key bg_color: Background color, should be PIL.ImageColor

        Name:
        :key name_size: Size of name, should be int
        :key name_pos: Static position of name, should be tuple
        :key name_center: Dynamic position of name, should be tuple

        Description:
        :key desc_pos: Position of description lines, should be tuple
        :key desc_center: Dynamic position of description, should be
        :key font: Font filepath, should be str
        """

        self.size = size
        self.img_size = img_size
        self.params = params

        self._check_params()

    def _check_params(self):
        # TODO: Check params
        # Checking bg color
        if 'bg_color' not in self.params.keys():
            self.params['bg_color'] = ImageColor.getrgb("#000000")

    def generate(self, icon: str, name: str, description: str):
        image = Image.new("RGB", self.size, self.params['bg_color'])

    def add_message(self, image: Image):
        pass

    def add_icon(self, image: Image):
        pass

    def add_name(self, image: Image):
        pass

    def add_description(self, image: Image):
        pass
