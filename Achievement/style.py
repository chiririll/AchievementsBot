import json
from zipfile import ZipFile


class Style:
    def __init__(self, style, lang='ENG'):
        zf = ZipFile(style, 'r')

        self.__style = json.loads(zf.read("style.json"))
        self.__attachments = {}
        self.lang = self.__set_lang(lang)

        for file in zf.filelist:
            path = file.filename.split('/', 1)
            if path[0] == "res" and '/' not in path[1] and len(path[1]) > 0:
                self.__attachments[path[1]] = zf.read(file.filename)

        zf.close()
        style.close()

    # Info #
    def get_info(self):
        info = [
            f"Style name: {self.__style['name']}",
            f"Created by {self.__style['author']}",
            f"Creation date: {self.__style['created']}"
        ]
        return '\n'.join(info)

    def get_name(self):
        return self.__style['name']
    # ==== #

    # Generator functions #
    def get_attachment(self, name):
        return self.__attachments.get(name, None)

    def get_string(self, key):
        # Finding key in localization dict
        # If lang is None or key not found -> returns key
        return self.__style['localization'][self.lang].get(key, key) if self.lang else key

    def get_color(self, key, default='#000000'):
        return self.__style['colors'].get(key, default)

    def get_size(self):
        return self.__style['size']

    def get_layer(self, index):
        return self.__style['layers'][index]

    def get_layers(self):
        return self.__style['layers']
    # =================== #

    # Private methods #
    def __set_lang(self, lang):
        # Checking languages and localization field
        if len(self.__style.get('localization', {}).keys()) == 0:
            return None

        # Finding language
        if lang in self.__style['localization'].keys():
            return lang

        return self.__style['localization'].keys()[0]
    # =============== #
