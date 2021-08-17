import json
import logging
from io import BytesIO
from typing import Optional, Dict, Any, IO, List, Union
from zipfile import ZipFile


logger = logging.getLogger(__name__)


class Style:

    def __init__(self, style: Union[str, BytesIO, IO], lang: str = 'ENG'):
        # Opening style file
        if type(style) is str:
            style = open(style, 'rb')

        self.__style: Dict[str, Any] = {}
        self.__attachments: Dict[str, Optional[bytes]] = {}
        self.__lang: Optional[str] = None

        # For .achst files
        def load_zip() -> None:
            zf = ZipFile(style, 'r')
            # Extracting style
            self.__style = json.loads(zf.read("style.json"))
            # Extracting attachments
            for file in zf.filelist:
                path = file.filename.split('/', 1)
                if path[0] == "res" and '/' not in path[1] and len(path[1]) > 0:
                    self.__attachments[path[1]] = zf.read(file.filename)
            # Closing zip
            zf.close()

        # For .achs files
        def load_json() -> None:
            self.__style = json.loads(style.read())

        def detect_type() -> str:
            t = 'achst'
            if style.read(1) == b'{':
                t = 'achs'
            style.seek(0)
            return t

        # Reading file
        if detect_type() == 'achst':
            load_zip()
        else:
            load_json()
        # Logging
        logger.info(f"Initializing style {self.__style['name']}")
        # Closing file
        style.close()
        # Checking language
        self.change_lang(lang)

    # Info #
    def get_info(self) -> str:
        info = [
            f"Style name: {self.__style['name']}",
            f"Created by {self.__style['author']}",
            f"Creation date: {self.__style['created']}"
        ]
        return '\n'.join(info)

    def get_name(self, lang: Optional[str] = None) -> str:
        if not lang:
            lang = self.__lang
        return self.__style['localization'].get(lang, {}).get('_name', self.__style['name'])

    def get_colors_info(self) -> Dict[str, str]:
        return self.__style['localization'].get(self.__lang, {}).get('@colors', {})

    def get_langs(self) -> List[str]:
        langs = list(self.__style['localization'].keys())
        if '_' in langs:
            langs.remove('_')
        return langs
    # ==== #

    # Configuration #
    def change_lang(self, lang: str) -> str:
        # Checking languages and localization field
        if len(self.__style['localization'].keys()) == 0:
            self.__lang = None
            return 'error'

        # Finding language
        if lang in self.__style['localization'].keys():
            self.__lang = lang
            return 'ok'

        self.__lang = self.__style['localization'].keys()[0]
        return 'warning'
    # ============= #

    # Generator functions #
    def get_attachment(self, name: str) -> Optional[bytes]:
        if not name:
            return None
        name = name.replace('@src/', '')
        return self.__attachments.get(name, None)

    def get_file(self, name: str, default: str = None) -> Union[BytesIO, str]:
        if not name:
            return default
        file = self.get_attachment(name)
        return BytesIO(file) if file else default

    def get_string(self, key: str, **strings) -> Optional[str]:
        if not key:
            return None
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
            string = string.replace(f"%{k}%", v if v else '')

        return string

    def get_color(self, key: str, default: str = '#000000') -> str:
        if not key:
            return default
        key = key.replace('@color/', '')
        return self.__style['colors'].get(key, default)

    def get_size(self) -> List[int]:
        return self.__style['size']

    def get_layer(self, index) -> Dict[str, Any]:
        return self.__style['layers'][index]

    def get_layers(self) -> List[Dict[str, Any]]:
        return self.__style['layers']

    # Replacing address strings
    def get_resource(self, path, **strings):
        if type(path) is not str:
            return path

        parts = path[1:].split('/', 1)
        if parts[0] == 'color':
            return self.get_color(parts[1], strings.get('default', '#000000'))
        elif parts[0] == 'text':
            return self.get_string(parts[1], **strings)
        elif parts[0] == 'src':
            return self.get_file(parts[1], strings.get('default'))
        else:
            return path

    # =================== #

    # Private methods #
    # =============== #
