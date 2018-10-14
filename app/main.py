#  def application(env, start_resp):
#      start_resp('200 OK', [ ('Content-Type', 'text/plain') ])
#      return [ 'Hello there!'.encode('utf-8') ]

import datetime
import json


def application(env, start_resp):
    status = '200 OK'
    headers = [('Content-Type', 'application/json')]  # response headers

    body = {
        'time': datetime.datetime.strftime(datetime.datetime.now(), "%H:%M:%S"),
        'url': env['wsgi.url_scheme']+'://'+env['HTTP_HOST']
    }

    start_resp(status, headers)
    return [json.dumps(body).encode('utf-8')]
