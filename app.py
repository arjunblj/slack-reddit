
import os

from flask import Flask, request, Response, redirect


app = Flask(__name__)


@app.route('/')
def hello():
    return 'hello!'


if __name__ == '__main__':
    app.run()
