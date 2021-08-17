import collections
from typing import DefaultDict, Tuple, Optional

from telegram.ext import BasePersistence
from telegram.ext.utils.types import UD, CDCData, BD, CD, ConversationDict

from DBHelper import Database


class DBHelperPersistence(BasePersistence):

    def __init__(self, database: Database, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DB = database

    # Chat Data #
    def update_chat_data(self, chat_id: int, data: CD) -> None:
        pass

    def get_chat_data(self) -> DefaultDict[int, CD]:
        return collections.defaultdict()
    # ========= #

    # Bot data #
    def update_bot_data(self, data: BD) -> None:
        pass

    def get_bot_data(self) -> BD:
        return {}
    # ======== #

    # Callback data #
    def update_callback_data(self, data: CDCData) -> None:
        pass

    def get_callback_data(self) -> Optional[CDCData]:
        pass
    # ============= #

    # User data #
    def update_user_data(self, user_id: int, data: UD) -> None:
        pass

    def get_user_data(self) -> DefaultDict[int, UD]:
        return collections.defaultdict()

    # ========= #

    # Conversation #
    def update_conversation(self, name: str, key: Tuple[int, ...], new_state: Optional[object]) -> None:
        pass

    def get_conversations(self, name: str) -> ConversationDict:
        return {}
    # ============= #
