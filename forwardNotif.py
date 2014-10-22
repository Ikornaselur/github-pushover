#!/usr/bin/python

from agithub import Github
from datetime import timedelta, datetime 
import httplib, urllib


TOKEN_FILE = 'token'
PUSHOVER_FILE = 'pushover'


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


def parse_message(reason, title):
    if reason == "mention" or reason == "team_mention":
        return "You were mentioned in {}".format(title)
    if reason == "assign":
        return "You were assigned to {}".format(title)
    if reason == "state_change":
        return "State changed on {}".format(title)
    if reason in ["subscribed", "manual", "comment"]:
        return "New comment on {}".format(title)
    return title


def main():
    user, passwd = read_values(TOKEN_FILE)
    push_user_key, push_app_key = read_values(PUSHOVER_FILE)

    g = Github(user, passwd)
    one_min_ago = (datetime.now() - timedelta(minutes=1)).strftime(
        "%Y-%m-%dT%H:%M:%SZ")
    notifications = get_notifications(one_min_ago, g)
    for notif in notifications:
        reason = notif['reason']
        title = notif['subject']['title']
        url = notif['subject']['url']
        message = parse_message(reason, title)
        push_message(push_user_key, push_app_key, 'Github', message, url)


if __name__ == '__main__':
    main()
