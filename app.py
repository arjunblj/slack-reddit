
import os
import praw

from flask import Flask, jsonify, request, Response


app = Flask(__name__)
Reddit = praw.Reddit(user_agent='slack-reddit-v1 by /u/arjunblj')

SORT_TYPES = {
    'hot': 'get_hot',
    'new': 'get_new',
    'top': 'get_top',
    'rising': 'get_rising'
}


def parse_reddit(subreddit, sort='hot', top_num=5):
    try:
        sub = Reddit.get_subreddit(subreddit)
        resp = getattr(sub, SORT_TYPES[sort])(limit=top_num)
        data = []
        for result in resp:
            data.append(dict(url=result.url, score=result.score, title=result.title))
        return dict(data=data)
    except praw.errors.InvalidSubreddit:
        return dict(data='Invalid Subreddit')


def parse_terms(terms):
    if len(terms) is 2:
        sort_type = terms[1]
        if sort_type in SORT_TYPES.keys():
            return parse_reddit(terms[0], sort_type)
    elif len(terms) is 3:
        try:
            sort_type, top_num = terms[1], int(terms[2])
            if sort_type in SORT_TYPES.keys() and isinstance(top_num, int):
                return parse_reddit(terms[0], sort_type, top_num)
        except:
            return dict(data='Invalid search')


@app.route('/search', methods=['post'])
def search():
    """i.e. /reddit nba rising 10
    """
    terms = request.values.get('text').split(' ')
    if len(terms) is 1:
        resp = parse_reddit(terms[0])
    else:
        try:
            resp = parse_terms(terms)
        except:
            resp = dict(data='Sorry, your request was incorrect')
    return jsonify(resp)


@app.route('/')
def hello():
    return 'hello!'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
