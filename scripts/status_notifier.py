import urllib.request
import json

def post_json(url, data):
    request = urllib.request.Request(url)
    request.add_header('Content-Type', 'application/json')
    f = urllib.request.urlopen(request, data)
    return f.status == 200


def notify_slack(url, name, msg):
    obj = {'text': msg}
    if name is not None:
        obj['username'] = name
    post_json(url
              , bytes(json.dumps(obj), 'utf-8'))


def notify(msg, name, targets):
    if 'slack' in targets:
        notify_slack(targets['slack'], name, msg)


def test():
    slack='https://hooks.slack.com/services/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'
    print(post_json('https://hooks.slack.com/services/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'
                    , bytes('{"text":"test message"}', 'utf-8')))

    print(notify_slack('https://hooks.slack.com/services/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'
                       , 'test bot', '{"text":"test message"}'))


if __name__ == '__main__':
    test()
