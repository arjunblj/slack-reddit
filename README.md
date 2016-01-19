# slack-reddit

Quick (and private) Reddit search via Slack.

<a href="https://slack.com/oauth/authorize?scope=commands&client_id=8225617457.18890826067"><img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x"></a>

![](http://i.imgur.com/Yohk8Zj.gif)

## Add to your team

1. In the Admin panel, go to **Custom Integrations** > **Slash Commands**.
2. Click on **Add Configuration**
3. Under **Integration Settings**, fill out:
  * Command: `/reddit`
  * URL: `https://reddit-slack.herokuapp.com/search`
  * Method: `POST`
  * Customize Name: `reddit`
  * For an image, use this Reddit logo (thanks guys, you rock!): `http://i.imgur.com/Ystfxa4.jpg`
  * In the **Autocomplete help text**, check "Show this command in the autocomplete list".
    * Description: `Search Reddit via Slack.`
    * Usage hint: `[subreddit] [sort] [results]`
  * Descriptive Label: `Search Reddit, really fast!`

Warning: There is some NSFW content that you can reach -- it's not in my hands. ¯\_(ツ)_/¯

## To run locally

```shell
$ pip install -r requirements.txt
```

```shell
$ python app.py
```
