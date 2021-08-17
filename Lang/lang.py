import json
import logging

from os import listdir
from os.path import isfile, join

from typing import Dict


# Logging
logger = logging.getLogger(__name__)


# Loading languages dicts into LANG_DICT
def __init_langs() -> Dict[str, dict]:
    folder = "Lang/langs"
    files = [f.split('.')[0] for f in listdir(folder) if isfile(join(folder, f))]
    dicts = [json.load(open(join(folder, d + ".json"), 'r', encoding='utf-8')) for d in files]
    return dict(zip(files, dicts))


# Loading languages
LANG_DICT = __init_langs()
LANG_NAME = json.load(open("Lang/languages.json", 'r', encoding='utf-8'))


# TODO: Replace address strings (e.g. @params.search)
def get(key: str, msg_lang: str = 'ENG', **params) -> str:
    """ Function for getting language string by key """
    def get_path(dictionary: dict, path: list, default: str = key) -> str:
        """ Recursive function for finding key """
        val = dictionary.get(path[0])
        if type(val) is dict:
            return get_path(val, path[1:])
        if type(val) is str:
            return val
        if type(val) is list:
            return '\n'.join(val)

        logger.warning(f"Can't find string \"{default}\" in language \"{msg_lang}\"")
        return default

    def replace_markers(string: str) -> str:
        """ Function for replacing markers """
        for p_key, p_val in params.items():
            string = string.replace(f"%{p_key}%", str(p_val))
        return string

    # Checking null
    if not msg_lang:
        msg_lang = 'ENG'

    return replace_markers(get_path(LANG_DICT.get(msg_lang, {}), key.split('.')))


def get_lang(lang_code: str, for_text: bool = False) -> str:
    """ Function for getting language name by it's code """
    if for_text:
        return LANG_NAME.get(lang_code, ['', lang_code])[1].lower()
    return ' '.join(LANG_NAME.get(lang_code, [lang_code]))


def get_langs() -> list:
    """ Function returns available languages """
    return list(LANG_DICT.keys())
