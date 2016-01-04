
import os

from flask import Flask, request, Response, redirect


app = Flask(__name__)


@app.route('/')
def hello():
    return 'hello!'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
