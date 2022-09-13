# -*- coding: utf-8 -*-
# __author__ = 'SnkrGao'
# __time__ = '2022/9/9 11:14'
from parseAttitude import *
from parseRepost import *
from parseComments import *

if __name__ == '__main__':
    weibo_id = 'your weibo mid'
    cookie = 'your cookie'
    parseattitude = parseAttitude(weibo_id=weibo_id, cookie=cookie)
    parseattitude.SpiderAttitude()
    parserepost = parseRepost(weibo_id=weibo_id, cookie=cookie)
    parserepost.SpiderTransmit()
    parsecomments = parseComments(weibo_id=weibo_id, cookie=cookie)
    parsecomments.main()
