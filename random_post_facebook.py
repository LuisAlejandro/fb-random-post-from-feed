#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# http://stackoverflow.com/questions/17197970/facebook-permanent-page-access-token

import sys
import json
from random import choice
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from datetime import datetime

from utils import utfize, html_unescape, filter_json_index_by_year

facebook_api_end = 'https://graph.facebook.com/156686441067299/feed'
facebook_access_token = ('EAAF0cGsgXS8BAMniHEKNzK5KPeaWcevyCbu8lwQH0Y'
                         'FWsLj5VWyvcEyknMh1IYmIxXpZCbJiZC6Slfg3rZBzm'
                         'R8ZCRpo52sHx7hCWVUXM4Jw3w3aOfU9ANSRZBLcXvFm'
                         'uEEBQSfHno51gvTAS7d1f0QtrYTxzqZBrSuGwr0q3cwAZDZD')
json_index_url = 'http://huntingbears.com.ve/static/json/index.json'

print('Starting publication of random post to Facebook')

current_timestamp = int(datetime.now().strftime('%Y%m%d%H%M%S'))
current_hour = int(datetime.now().strftime('%H'))

if current_hour not in [9, 13, 15, 22]:
    print('Script wasnt called in a recommended hour. Aborting.')
    sys.exit(0)

json_index_content = json.loads(str(urlopen(json_index_url).read(), 'utf-8'))
json_index_filtered = filter_json_index_by_year(json_index_content)

if not json_index_filtered:
    print('There are no posts to publish. Aborting.')
    sys.exit(0)

random_post_id = choice(list(json_index_filtered.keys()))
random_post_title = json_index_filtered[random_post_id]['title']
random_post_title = utfize(html_unescape(random_post_title))
random_post_url = utfize('{0}#{1}'.format(
    json_index_filtered[random_post_id]['url'],
    current_timestamp))

facebook_api_data = {'message': random_post_title,
                     'link': random_post_url,
                     'access_token': facebook_access_token}

http_request = Request(url=facebook_api_end, method='POST',
                       data=urlencode(facebook_api_data).encode())

count = 0
while count < 6:
    try:
        result = json.loads(str(urlopen(http_request).read(), 'utf-8'))
    except Exception as e:
        print('There was an error publishing: {0}'.format(e))
        count += 1
        continue

    if 'error' in result:
        count += 1
        continue

    print('Successfully published!: {0}'.format(random_post_url))
    break
