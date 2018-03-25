#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'du'

import hashlib
import re

def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

def extract_num(value):
    match_com = re.match('.*?(\d+).*', value)
    if match_com:
        num = int(match_com.group(1))
    else:
        num = 0
    return num

if __name__ == '__main__':
    print(get_md5('http://www.baidu.com'))
