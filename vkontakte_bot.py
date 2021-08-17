import logging
import random

import requests
import vk_api
from vk_api import bot_longpoll
from vk_api.bot_longpoll import VkBotEventType
from os import environ as env
import Lang
import Styles
import Tools
from Achievement import Achievement


# Logging
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# Context #
CHAT_DATA = {}
vk = None


def get_chat_data(key: str, obj: dict, default=None):
    return CHAT_DATA.get(obj['peer_id'], {}).get(key, default)


def edit_chat_data(key: str, val, obj: dict, default=None) -> None:
    # TODO: save to db
    CHAT_DATA.update((obj['peer_id'][key], val))
# ======= #


# API #
def reply_text(text: str, obj: dict) -> None:
    vk.messages.send(peer_id=obj['peer_id'], random_id=random.randint(0, 100000), message=text)


def reply_photo(photo, obj) -> None:
    server_url = vk.photos.getMessagesUploadServer(peer_id=obj['peer_id'])['upload_url']
    upload_req = requests.post(server_url, files={
        'photo': ('photo.png', photo.read(), 'image/png')
    }).json()
    photo = vk.photos.saveMessagesPhoto(**upload_req)[0]
    photo = 'photo' + str(photo['owner_id']) + '_' + str(photo['id']) + '_' + photo['access_key']

    # Sending achievement to user
    vk.messages.send(peer_id=obj['peer_id'], random_id=random.randint(0, 100000), attachment=photo)
# === #


def handle_button(obj: dict) -> None:
    pass


def handle_command(obj: dict) -> None:
    def unknown_command():
        reply_text(Lang.get('command.null', get_chat_data('lang', obj)), obj)

    commands = {}

    command = obj['text'][1:].split(' ', 1)[0]
    commands.get(command, unknown_command)()


def handle_attachment(obj: dict):
    # edit_chat_data('image_url', get_photo(obj), obj)
    # reply_text(Lang.get("achievement.require_name", get_chat_data('lang', obj)), obj)
    reply_text("No", obj)


def get_photo(obj):
    for a in obj['attachments']:
        if a['type'] == 'photo':
            sizes = a['photo']['sizes']
            return sizes[1 if len(sizes) > 1 else 0]['url']
    return None


def create_achievement(obj: dict) -> None:
    lang = get_chat_data('lang', obj)

    # Checking name & description
    vals = Achievement.parse_message(obj['text'])
    for err in Achievement.check_values(**vals):
        reply_text(Lang.get(err, lang, **Achievement.LIMITS), obj)
        vals = None
    if not vals:
        return

    # Icon & style
    image = get_photo(obj)
    if not image and get_chat_data('image_url', obj):
        image = get_chat_data('image_url', obj)
        edit_chat_data('image_url', None, obj)

    vals['icon'] = Tools.download_image(image or Tools.search_image(vals['name']))
    vals['style'] = Styles.get(get_chat_data('style', obj))

    # Setting language
    ach_lang = get_chat_data('ach_lang', obj, 'RUS')
    if vals['style'].change_lang(ach_lang) != 'ok':
        reply_text(Lang.get('error.achievement.no_lang', lang, lang=ach_lang, style=vals['style'].get_name(lang)), obj)

    ach = Achievement(**vals)
    gen = ach.generate()
    if type(gen) is str:
        reply_text(Lang.get(gen, lang), obj)
    else:
        reply_photo(gen, obj)

    # TODO: add buttons (other images and styles)


def main() -> None:
    vk_session = vk_api.VkApi(token=env.get('VK_TOKEN'))
    global vk
    vk = vk_session.get_api()

    long_poll = vk_api.bot_longpoll.VkBotLongPoll(
        vk=vk_session,
        group_id=int(env.get('VK_GROUP_ID')),
        wait=int(env.get('VK_TIMEOUT', 40))
    )

    for event in long_poll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            obj = event.object.message
            # Reading message
            vk.messages.markAsRead(messages_ids=[obj['id']], peer_id=obj['peer_id'])

            if 'payload' in obj.keys():
                handle_button(obj)
            elif len(obj.get('text', '')) > 0:
                if obj['text'][0] == '/':
                    handle_command(obj)
                else:
                    create_achievement(obj)
            elif len(obj['attachments']) > 0:
                handle_attachment(obj)


if __name__ == "__main__":
    logger.info("Starting VK bot")
    main()
