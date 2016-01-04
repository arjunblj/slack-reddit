
import os
import praw

from flask import Flask, request, Response, redirect


app = Flask(__name__)
Reddit = praw.Reddit(user_agent='SlackRedditv1 by /u/arjunblj')


@app.route('/search', methods=['post'])
def search():
    resp = 'hi!'
    return Response(resp, content_type='text/plain; charset=utf-8')


@app.route('/')
def hello():
    return 'hello!'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
