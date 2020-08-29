from flask import Flask, send_file
from achievement import Achievement
from os import environ as env

app = Flask(__name__)


@app.route('/new/<name>')
def new(name):
    ach = Achievement(name)
    return send_file(ach.get(), mimetype='image/PNG')


@app.route('/vk')
def vk():
    return 'ok'


@app.route('/telegram')
def telegram():
    return 'ok'


if __name__ == "__main__":
    app.run()
