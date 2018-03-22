#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from urllib.parse import quote
from html.parser import HTMLParser


def html_unescape(_string):
    return HTMLParser().unescape(_string)


def escape(_string):
    return quote(_string.encode(), safe='~')


def utfize(_string):
    return str(_string)


def filter_json_index_by_year(json_index_content):
    json_index_filtered = {}
    current_year = int(datetime.now().strftime('%Y'))
    for pid, data in json_index_content.items():
        post_date = datetime.strptime(data['date'][:-6], '%Y-%m-%dT%H:%M:%S')
        post_year = int(post_date.strftime('%Y'))
        if post_year >= (current_year - 2):
            json_index_filtered[pid] = data
    return json_index_filtered
