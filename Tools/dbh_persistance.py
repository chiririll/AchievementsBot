import collections
import json
from typing import DefaultDict, Tuple, Optional

from telegram.ext import BasePersistence
from telegram.ext.utils.types import UD, CDCData, BD, CD, ConversationDict

from DBHelper import Database


class DBHelperPersistence(BasePersistence):

    def __init__(self, database: Database, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DB = database

    # Closing connection
    def flush(self) -> None:
        self.DB.end()

    # Chat Data #
    def update_chat_data(self, chat_id: int, data: CD) -> None:
        self.DB.insert_or_update('t_chat_data', id=chat_id, val=json.dumps(data))

    def get_chat_data(self) -> DefaultDict[int, CD]:
        cd = collections.defaultdict(dict)
        for chat in self.DB.select('t_chat_data', '*'):
            cd[chat[0]] = json.loads(chat[1])
        return cd
    # ========= #

    # Bot data (t_data.type = 0) #
    def update_bot_data(self, data: BD) -> None:
        self.DB.insert_or_update('t_data', type=0, val=json.dumps(data))

    def get_bot_data(self) -> BD:
        bd = self.DB.select('t_data', '*', "WHERE type = 0")
        if len(bd) > 0:
            return json.loads(bd[0][1])
        return {}
    # ======== #

    # Callback data (t_data.type = 1) #
    def update_callback_data(self, data: CDCData) -> None:
        pass

    def get_callback_data(self) -> Optional[CDCData]:
        pass
    # ============= #

    # User data #
    def update_user_data(self, user_id: int, data: UD) -> None:
        self.DB.insert_or_update('t_user_data', id=user_id, val=json.dumps(data))

    def get_user_data(self) -> DefaultDict[int, UD]:
        ud = collections.defaultdict(dict)
        for user in self.DB.select('t_user_data', '*'):
            ud[user[0]] = json.loads(user[1])
        return ud
    # ========= #

    # Conversation #
    def update_conversation(self, name: str, key: Tuple[int, ...], new_state: Optional[object]) -> None:
        pass

    def get_conversations(self, name: str) -> ConversationDict:
        pass
    # ============= #
