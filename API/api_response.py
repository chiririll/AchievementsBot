from io import BytesIO


class Response:
    keyboard = None
    message = ""
    images = []     # BytesIO
    img_urls = []   # URLs

    def __init__(self, **params):
        """
        Class for sending response to API
        :param params: Fields of response
        """
        if 'keyboard' in params.keys():
            self.keyboard = params['keyboard']
        if 'message' in params.keys():
            self.message = params['message']
        if 'images' in params.keys():
            self.images = params['images']
        if 'img_urls' in params.keys():
            self.img_urls = params['img_urls']

    def add_image(self, image: BytesIO):
        self.images.append(image)

    def add_img_url(self, img_url: str):
        self.img_urls.append(img_url)
