import json
from zipfile import ZipFile


class Style:
    def __init__(self, style, lang='ENG'):
        zf = ZipFile(style, 'r')

        self.__style = json.loads(zf.read("style.json"))
        self.__attachments = {}
        self.__lang = None

        # Checking language
        self.change_lang(lang)

        # Extracting attachments
        for file in zf.filelist:
            path = file.filename.split('/', 1)
            if path[0] == "res" and '/' not in path[1] and len(path[1]) > 0:
                self.__attachments[path[1]] = zf.read(file.filename)

        zf.close()
        if type(style) is not str:
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

    def get_colors_info(self):
        return self.__style['localization'].get(self.__lang, {}).get('@colors', {})

    def get_langs(self):
        langs = list(self.__style['localization'].keys())
        if '_' in langs:
            langs.remove('_')
        return langs
    # ==== #

    # Configuration #
    def change_lang(self, lang):
        # Checking languages and localization field
        if len(self.__style['localization'].keys()) == 0:
            self.__lang = None
            return 'error.style.lang.null'

        # Finding language
        if lang in self.__style['localization'].keys():
            self.__lang = lang
            return 'ok'

        self.__lang = self.__style['localization'].keys()[0]
        return 'warning.style.lang.unsupported'
    # ============= #

    # Generator functions #
    def get_attachment(self, name: str):
        return self.__attachments.get(name, None)

    def get_string(self, key: str, **strings):
        key = key.replace('@text/', '')
        if key[0] == '@':
            return key

        # Finding key in localization dict
        # If lang is None or key not found -> returns key
        string = self.__style['localization'].get(self.__lang, {}).get(key, None)

        # Finding in common languages
        if not string:
            string = self.__style['localization'].get('_', {}).get(key, key)

        # Handling name & description
        for k, v in strings.items():
            string = string.replace(f"%{k}%", v)

        return string

    def get_color(self, key: str, default='#000000'):
        key = key.replace('@color/', '')
        return self.__style['colors'].get(key, default)

    def get_size(self):
        return self.__style['size']

    def get_layer(self, index):
        return self.__style['layers'][index]

    def get_layers(self):
        return self.__style['layers']

    # Replacing address strings
    def handle_value(self, val, **strings):
        if type(val) is not str:
            return val

        parts = val[1:].split('/', 1)
        if parts[0] == 'color':
            return self.get_color(parts[1], strings.get('default', '#000000'))
        elif parts[0] == 'text':
            return self.get_string(parts[1], **strings)
        else:
            return val

    # =================== #

    # Private methods #
    # =============== #
