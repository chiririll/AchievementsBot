from threading import Thread
from flask import Flask, request
from os import environ as env
from API import VK

app = Flask(__name__)
threads = []


@app.route('/vk', methods=['POST'])
def vk_api():
    clear_threads()

    req = request.get_json()

    # Returning confirmation code
    if req['type'] == 'confirmation':
        return env['VK_CONFIRM']
    # Checking secret
    elif req['secret'] != env['VK_SECRET']:
        return 'not vk'

    vk = VK(req)
    threads.append(Thread(target=vk.handle))
    threads[-1].start()

    print(threads)

    return 'ok'


@app.route('/telegram')
def telegram():
    clear_threads()

    return 'ok'


def clear_threads():
    i = 0
    while i < len(threads):
        if not threads[i].isAlive():
            del threads[i]
        else:
            i += 1


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
