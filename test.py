# -*- coding: utf-8 -*-
#
# Please refer to AUTHORS.md for a complete list of Copyright holders.
# Copyright (C) 2020-2022 Luis Alejandro Martínez Faneyth.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import time
import datetime
from urllib.request import urlopen
from html import unescape
from random import choice

from atoma import parse_rss_bytes
from pyfacebook import GraphAPI


count = 0
json_index_content = {}
access_token = os.environ.get('FACEBOOK_ACCESS_TOKEN')
page_id = os.environ.get('FACEBOOK_PAGE_ID')
feed_url = os.environ.get('FEED_URL')
max_post_age = int(os.environ.get('MAX_POST_AGE', 365))

if not feed_url:
    raise Exception('No FEED_URL provided.')

if not page_id:
    raise Exception('No FACEBOOK_PAGE_ID provided.')

graph = GraphAPI(access_token=access_token, version="13.0")

feed_data = parse_rss_bytes(urlopen(feed_url).read())
today = datetime.datetime.now()
max_age_delta = today - datetime.timedelta(days=max_post_age)
max_age_timestamp = int(max_age_delta.strftime('%Y%m%d%H%M%S'))

for post in feed_data.items:

    item_timestamp = post.pub_date.strftime('%Y%m%d%H%M%S')

    if int(item_timestamp) >= max_age_timestamp:
        json_index_content[item_timestamp] = {
            'title': post.title,
            'url': post.guid,
            'date': post.pub_date
        }

random_post_id = choice(list(json_index_content.keys()))
random_post_title = json_index_content[random_post_id]['title']
status_link = '{0}#{1}'.format(
    json_index_content[random_post_id]['url'],
    today.strftime('%Y%m%d%H%M%S'))
data = {'message': unescape(random_post_title), 'link': status_link}

fb = graph.post_object(object_id=page_id,
                       connection='feed',
                       data=data)
time.sleep(10)
graph.delete_object(object_id=fb['id'])
