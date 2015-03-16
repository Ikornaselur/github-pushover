#!/usr/bin/python

from agithub import Github
from datetime import timedelta, datetime 
from os import path
from json import dumps
import httplib, urllib


DIR_NAME = path.dirname(path.realpath(__file__))
TOKEN_FILE = DIR_NAME + '/token'
PUSHOVER_FILE = DIR_NAME + '/pushover'

def read_values(file_name):
    with open(file_name) as f:
        return tuple(f.read().strip().split(','))


def get_notifications(after, github):
    if after:
        status, data = github.notifications.get(since=after)
    else:
        status, data = github.notifications.get()

    if status == 200:
        return data
    else:
        print "Error! Status was {}".format(status)


def push_message(user_key, app_token, title, message, url):
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
        urllib.urlencode({
            "token": app_token,
            "user": user_key,
            "message": message,
            "title": title,
            "url": url
        }), {"Content-type": "application/x-www-form-urlencoded"})
    conn.getresponse()


def get_comment(comment_url, github):
    comment = github.client.get(comment_url[comment_url.index('m/')+1:])
    commenter = comment[1]['user']['login']
    body = comment[1]['body']
    return commenter, body


def parse_url(url):
    parts = url.split('/')
    if parts[-2] == 'pulls':
        return "https://github.com/{}/{}/pull/{}".format(
            parts[-4], parts[-3], parts[-1])
    if parts[-2] == 'issues':
        return "https://github.com/{}/{}/issues/{}".format(
            parts[-4], parts[-3], parts[-1])
    return url 


def main():
    user, passwd = read_values(TOKEN_FILE)
    push_user_key, push_app_key = read_values(PUSHOVER_FILE)

    g = Github(user, passwd)
    one_min_ago = (datetime.now() - timedelta(minutes=1)).strftime(
        "%Y-%m-%dT%H:%M:%SZ")
    notifications = get_notifications(one_min_ago, g)

    for notif in notifications:
        user, body = get_comment(notif['subject']['latest_comment_url'], g)
        ntype = notif['subject']['type']
        ntitle = notif['subject']['title']

        notification = {
            'title': '{user} commented on {ntype}: {ntitle}'.format(
            user=user, ntype=ntype, ntitle=ntitle),
            'body': body,
            'url': parse_url(notif['subject']['url'])
        };

        push_message(push_user_key, push_app_key,
            notification['title'], notification['body'], notification['url'])


if __name__ == '__main__':
    main()
