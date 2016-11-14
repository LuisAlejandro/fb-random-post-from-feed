#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from random import getrandbits, choice
import base64
import hmac
import hashlib
from urllib.request import urlopen, Request
from urllib.parse import quote, urlencode
from html.parser import HTMLParser
from datetime import datetime


def html_unescape(_string):
    return HTMLParser().unescape(_string)


def escape(_string):
    return quote(_string.encode(), safe='~')


def utfize(_string):
    return str(_string)

TWITTER_API_VERSION = '1.0'
TWITTER_API_METHOD = 'HMAC-SHA1'
TWITTER_API_END = 'https://api.twitter.com/1.1/statuses/update.json'
TWITTER_CONSUMER_KEY = 'EfRsYNSXgd62lFtuP1RahQ'
TWITTER_CONSUMER_SECRET = '5EAk7IYlUQe3GX00bONoHx0fDJbuVUYMMDfEbbIsuY'
TWITTER_OAUTH_TOKEN = '320430429-896na1d2phjByw67KI3jr1poGtW5V2jJcZp9Zp1x'
TWITTER_OAUTH_SECRET = 'pAw4XsOjqBBOqaeLw7TtnwHQrY12dLdktRZ9GQyMyGwoA'
JSON_URL = 'http://huntingbears.com.ve/static/json/index.json'

print('Iniciando publicación de artículo aleatorio en Twitter.')

if int(datetime.now().strftime('%H')) % 4 == 0:

    JSON_CONTENT = json.loads(str(urlopen(JSON_URL).read(), 'utf-8'))
    JSON_CONTENT = {j: i for j, i in JSON_CONTENT.items() if int(datetime.strptime(i['date'][:-6], '%Y-%m-%dT%H:%M:%S').strftime('%Y')) >= (int(datetime.now().strftime('%Y'))-1)}
    RANDOM_POST = choice(list(JSON_CONTENT.keys()))
    RANDOM_POST_TITLE = utfize(html_unescape(JSON_CONTENT[RANDOM_POST]['title'][:113]+'...'))
    RANDOM_POST_LINK = utfize(JSON_CONTENT[RANDOM_POST]['url']+'#'+datetime.now().strftime('%Y%m%d%H%M%S'))

    TWITTER_STATUS = RANDOM_POST_TITLE+' '+RANDOM_POST_LINK

    SIGNATURE_TIMESTAMP = datetime.now().strftime('%s')
    SIGNATURE_ONCE = str(getrandbits(64))
    SIGNATURE_BASE_STRING_AUTH = {}
    SIGNATURE_BASE_STRING_AUTH['status'] = TWITTER_STATUS
    SIGNATURE_BASE_STRING_AUTH['oauth_consumer_key'] = TWITTER_CONSUMER_KEY
    SIGNATURE_BASE_STRING_AUTH['oauth_nonce'] = SIGNATURE_ONCE
    SIGNATURE_BASE_STRING_AUTH['oauth_signature_method'] = TWITTER_API_METHOD
    SIGNATURE_BASE_STRING_AUTH['oauth_timestamp'] = SIGNATURE_TIMESTAMP
    SIGNATURE_BASE_STRING_AUTH['oauth_token'] = TWITTER_OAUTH_TOKEN
    SIGNATURE_BASE_STRING_AUTH['oauth_version'] = TWITTER_API_VERSION

    SIGNATURE_BASE_STRING_AUTH = [escape(k)+'='+escape(v) for k, v in sorted(SIGNATURE_BASE_STRING_AUTH.items())]
    SIGNATURE_BASE_STRING_AUTH = '&'.join(SIGNATURE_BASE_STRING_AUTH)

    SIGNATURE_BASE_STRING = 'POST&'+escape(TWITTER_API_END)+'&'+escape(SIGNATURE_BASE_STRING_AUTH)
    SIGNATURE_KEY = TWITTER_CONSUMER_SECRET+'&'+escape(TWITTER_OAUTH_SECRET)

    OAUTH_HMAC_HASH = hmac.new(SIGNATURE_KEY.encode(), SIGNATURE_BASE_STRING.encode(), hashlib.sha1)
    OAUTH_SIGNATURE = base64.b64encode(OAUTH_HMAC_HASH.digest()).decode()

    OAUTH_HEADER = {}
    OAUTH_HEADER['oauth_consumer_key'] = TWITTER_CONSUMER_KEY
    OAUTH_HEADER['oauth_nonce'] = SIGNATURE_ONCE
    OAUTH_HEADER['oauth_signature'] = OAUTH_SIGNATURE
    OAUTH_HEADER['oauth_signature_method'] = TWITTER_API_METHOD
    OAUTH_HEADER['oauth_timestamp'] = SIGNATURE_TIMESTAMP
    OAUTH_HEADER['oauth_token'] = TWITTER_OAUTH_TOKEN
    OAUTH_HEADER['oauth_version'] = TWITTER_API_VERSION

    OAUTH_HEADER = [escape(k)+'="'+escape(v)+'"' for k, v in sorted(OAUTH_HEADER.items())]
    OAUTH_HEADER = ', '.join(OAUTH_HEADER)
    OAUTH_HEADER = 'OAuth '+OAUTH_HEADER

    HTTP_REQUEST = Request(url=TWITTER_API_END,
                           data=urlencode({'status': TWITTER_STATUS}).encode(),
                           headers={'Authorization': OAUTH_HEADER,
                                    'Content-Type': 'application/x-www-form-urlencoded'})
    while True:

        RESULT = json.loads(str(urlopen(HTTP_REQUEST).read(), 'utf-8'))

        if 'errors' not in RESULT:
            print('Publicación exitosa: '+RANDOM_POST_LINK)
            break
