
import os
import praw

from flask import Flask, redirect, request, Response


app = Flask(__name__)
Reddit = praw.Reddit(user_agent='slack-reddit-v1 by /u/arjunblj')

SORT_TYPES = {
    'hot': 'get_hot',
    'new': 'get_new',
    'top': 'get_top',
    'rising': 'get_rising'
}


def _create_response(text):
    """Returns a utf-8 encoded text response.
    """
    return Response(text, content_type='text/plain; charset=utf-8')


def _parse_options(options):
    """Returns a Response after validating the input.
    """
    if options[1] in SORT_TYPES.keys():
        sort_type = options[1]
        if len(options) > 2:
            subreddit, sort_type, num_results = options
            try:
                num_results = int(num_results)
                return fetch_posts(subreddit, sort_type, num_results)
            except ValueError:
                # Third option is invalid.
                response_text = ("Sorry! `%s` isn't a valid sorting number. Try `/reddit %s %s 5`"
                                 % (subreddit, sort_type, num_results))
                return _create_response(response_text)
        else:
            # No option for results to return.
            return fetch_posts(options[0], sort_type)
    else:
        if isinstance(options[1], int):
            # For the case that someone passes `/reddit [subreddit] [sort_num]`
            return fetch_posts(options[0], 'hot', options[1])
        else:
            return _create_response('Invalid search. Try `/reddit aww top 5` or `/reddit help`.')


def _get_post_header(subreddit, sort, top_num):
    """Formats the top heading to make it a bit more readable.
    """
    url = 'http://reddit.com/r/' + subreddit
    if sort == 'new':
        heading = '%s Newest Posts from' % (top_num)
    elif sort == 'top':
        heading = 'Top %s Posts from' % (top_num)
    elif sort == 'rising':
        heading = '%s Fastest Rising Posts' % (top_num)
    else:
        heading = '%s Hottest Posts' % (top_num)
    heading += ' <%s|/r/%s>\n' % (url, subreddit)
    return heading


def fetch_posts(subreddit, sort='hot', top_num=5):
    """Fetch post information from a subreddit given the options.
    """
    try:
        sub = Reddit.get_subreddit(subreddit)
        resp = getattr(sub, SORT_TYPES[sort])(limit=top_num)
        data = _get_post_header(subreddit, sort, top_num)
        for i, post in enumerate(resp):
            post_number = i + 1
            data += ('%s. *[%s]* <%s|%s>\n' %
                     (post_number, post.score, post.url, post.title))
        return _create_response(data)
    except praw.errors.InvalidSubreddit:
        return _create_response('Specify a subreddit that exists!')


def help_option():
    """Return text for `/reddit help`
    """
    help_text = """In order to use, you must specify a subreddit and can specify the type (hot [default], rising, new, or top), the number of results displayed or both! Some valid queries:
    `/reddit aww 5`
    `/reddit nba`
    `/reddit oddlysatisfying new 4`
Tweet @arjunblj if you have any other questions (or bugs) -- enjoy!"""
    return Response(help_text, content_type='text/plain; charset=utf-8')


@app.route('/search', methods=['post'])
def search():
    """i.e. /reddit nba rising 10
    """
    options = request.values.get('text').split(' ')
    if not options[0]:
        _create_response('You need to specify an option: try `/reddit aww top 5`.')
    elif len(options) is 1:
        if options[0] == 'help':
            return help_option()
        else:
            return fetch_posts(options[0])
    else:
        try:
            return _parse_options(options)
        except:
            return _create_response('Sorry, your request was incorrect.')


@app.route('/')
def hello():
    return redirect('https://github.com/arjunblj/slack-reddit')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
