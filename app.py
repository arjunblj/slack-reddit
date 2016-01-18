
import os
import praw

from flask import Flask, jsonify, redirect, request, Response


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
        data = ''
        for i, post in enumerate(resp):
            post_number = i + 1
            data += ("%s. *[%s]* <%s|%s>\n" % (post_number, post.score, post.url, post.title))
        return Response(data, content_type='text/plain; charset=utf-8')
    except praw.errors.InvalidSubreddit:
        return Response('Specify a subreddit that exists!', content_type='text/plain; charset=utf-8')


def help_option():
    help_text = """In order to use, you must specify a subreddit and can specify the type (hot [default], rising, new, or top), the number of results displayed or both! Some valid queries:
    */reddit nba 5
    */reddit nfl rising 12
    */reddit oddlysatisfying rising 12
Tweet @arjunblj if you have any other questions (or bugs) -- enjoy!"""
    return Response(help_text, content_type='text/plain; charset=utf-8')


def parse_terms(terms):
    if len(terms) is 2:
        option = terms[1]
        if option in SORT_TYPES.keys():
            return parse_reddit(terms[0], option)
        else:
            try:
                option = int(option)
                return parse_reddit(terms[0], 'hot', option)
            except ValueError:
                return Response('Invalid search, check your options.',
                    content_type='text/plain; charset=utf-8')
    elif len(terms) is 3:
        sort_type, top_num = terms[1], int(terms[2])
        if sort_type in SORT_TYPES.keys() and isinstance(top_num, int):
            return parse_reddit(terms[0], sort_type, top_num)
        else:
            return Response('Invalid search option. Try: hot (default), new, rising, or top.')


@app.route('/search', methods=['post'])
def search():
    """i.e. /reddit nba rising 10
    """
    terms = request.values.get('text').split(' ')
    if len(terms) is 0 or not terms[0]:
        return Response('You need to specify an option: try /reddit nba.', content_type='text/plain; charset=utf-8')
    elif len(terms) is 1:
        if terms[0] == 'help':
            return help_option()
        else:
            return parse_reddit(terms[0])
    else:
        try:
            return parse_terms(terms)
        except:
            return Response('Sorry, your request was incorrect', content_type='text/plain; charset=utf-8')


@app.route('/')
def hello():
    return redirect('https://github.com/arjunblj/slack-reddit')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
