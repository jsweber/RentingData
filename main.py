#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'du'

from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(['scrapy', 'crawl', 'lianjia'])
execute(['scrapy', 'crawl', 'liepinv2.0'])
