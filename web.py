from flask import Flask, send_file, request

from Achievement import Achievement
from API import VK

app = Flask(__name__)


@app.route('/new/<name>')
def new(name):
    ach = Achievement(name)
    return send_file(ach.get(), mimetype='image/PNG')


@app.route('/vk', methods=['POST'])
def vk_api():
    vk = VK(request.get_json())
    return vk.get_response()


@app.route('/telegram')
def telegram():
    return 'ok'


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
