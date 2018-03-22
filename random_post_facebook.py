#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# http://stackoverflow.com/questions/17197970/facebook-permanent-page-access-token

import json
from random import choice
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from datetime import datetime
from html.parser import HTMLParser


def html_unescape(_string):
    return HTMLParser().unescape(_string)


def utfize(_string):
    return str(_string).encode('utf-8')

FACEBOOK_API_END = 'https://graph.facebook.com/156686441067299/feed'
FACEBOOK_ACCESS_TOKEN = 'EAAF0cGsgXS8BAEGqIAv9MBVQVVO8Sah2xcwuitg4kFbp0p71iPARuKQgE0cyjk1Wmrz5Wpf3CAczPbPkHKhAaHoiikgC9RQSakWjthib1J1wX6o0gdrI5PjgvufJmvwbady0DZB8QZCaM6hNLn'
JSON_URL = 'http://huntingbears.com.ve/static/json/index.json'

print('Iniciando publicación de artículo aleatorio en Facebook.')

if int(datetime.now().strftime('%H')) % 3 == 0:

    JSON_CONTENT = json.loads(str(urlopen(JSON_URL).read(), 'utf-8'))
    JSON_CONTENT = {j: i for j, i in JSON_CONTENT.items() if int(datetime.strptime(i['date'][:-6], '%Y-%m-%dT%H:%M:%S').strftime('%Y')) >= (int(datetime.now().strftime('%Y'))-1)}
    RANDOM_POST = choice(list(JSON_CONTENT.keys()))
    RANDOM_POST_TITLE = utfize(html_unescape(JSON_CONTENT[RANDOM_POST]['title']))
    RANDOM_POST_LINK = utfize(JSON_CONTENT[RANDOM_POST]['url']+'#'+datetime.now().strftime('%Y%m%d%H%M%S'))

    FACEBOOK_API_DATA = {'message': RANDOM_POST_TITLE,
                         'link': RANDOM_POST_LINK,
                         'access_token': FACEBOOK_ACCESS_TOKEN}

    HTTP_REQUEST = Request(url=FACEBOOK_API_END, method='POST',
                           data=urlencode(FACEBOOK_API_DATA).encode())

    while True:

        RESULT = json.loads(str(urlopen(HTTP_REQUEST).read(), 'utf-8'))

        if 'error' not in RESULT:
            print('Publicación exitosa: %s' % RANDOM_POST_LINK)
            break
