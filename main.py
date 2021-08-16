import logging
import time
from threading import Thread
from os import environ as env


# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# Thread starters #
def telegram_thread():
    while True:
        import telega
        logger.info("Starting telegram thread")
        try:
            telega.main()
        except Exception as e:
            logger.error(f"Telegram thread error: {e}")
        time.sleep(env.get("THREAD_DELAY", 5))
        del telega


def vk_thread():
    while True:
        import vk
        logger.info("Starting vk thread")
        try:
            vk.main()
        except Exception as e:
            logger.error(f"Vk thread error: {e}")
        time.sleep(env.get("THREAD_DELAY", 5))
        del vk
# =============== #


THREADS = [
    Thread(name="Telegram", target=telegram_thread, daemon=True),
    Thread(name="Vk", target=vk_thread, daemon=True)
]


if __name__ == "__main__":
    for thread in THREADS:
        thread.start()
    while True:
        pass
