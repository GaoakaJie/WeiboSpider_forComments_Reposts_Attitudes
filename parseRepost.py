# -*- coding: utf-8 -*-
# __author__ = 'SnkrGao'
# __time__ = '2022/9/9 11:02'
import requests
import os
import time
import csv

class parseRepost():
    def __init__(self, cookie, weibo_id):
        self.cookie = cookie
        self.weibo_id = weibo_id
        self.referer = 'https://m.weibo.cn/detail/' + weibo_id
        self.headers = {
<<<<<<< HEAD
            'Accept':'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
=======
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
>>>>>>> 15457c8d2b3f91e9250ad082455968b4ea355dc3
            'referer': self.referer,
            'cookie': self.cookie,
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.36'
        }

    def SpiderTransmit(self):
        """
        # 爬取该微博id下所有转发人的信息
        """
        page_num = 1
        # 构造初始转发的url
        initial_url = 'https://m.weibo.cn/api/statuses/repostTimeline?id=' + self.weibo_id + '&page=' + str(page_num)
        response = requests.get(initial_url, headers=self.headers).json()
        while response['ok'] == 1:
            transmit_id, transmit_user_id, transmit_user_screen_name = [], [], []
<<<<<<< HEAD
            try:
                results_lines = []
                data_list = response['data']['data']
                n = len(data_list)
                for i in range(n):
                    data = data_list[i]
                    # transmit_id.append(data['id'])
                    # transmit_user_id.append(data['user']['id'])
                    # transmit_user_screen_name.append(data['user']['screen_name'])
                    results_lines.append(
                        (self.weibo_id, data['id'], data['user']['id'], data['user']['screen_name'], data['raw_text']))
                self.CsvPipeLineTransmit(results_lines)
                time.sleep(2)
                page_num += 1
                initial_url = 'https://m.weibo.cn/api/statuses/repostTimeline?id=' + self.weibo_id + '&page=' + str(
                    page_num)
                response = requests.get(initial_url, headers=self.headers).json()
            except Exception as e:
                print(e)
=======
            results_lines = []
            data_list = response['data']['data']
            n = len(data_list)
            for i in range(n):
                data = data_list[i]
                # transmit_id.append(data['id'])
                # transmit_user_id.append(data['user']['id'])
                # transmit_user_screen_name.append(data['user']['screen_name'])
                results_lines.append(
                    (self.weibo_id, data['id'], data['user']['id'], data['user']['screen_name'], data['raw_text']))
            self.CsvPipeLineTransmit(results_lines)
            time.sleep(2)
            page_num += 1
            initial_url = 'https://m.weibo.cn/api/statuses/repostTimeline?id=' + self.weibo_id + '&page=' + str(
                page_num)
            response = requests.get(initial_url, headers=self.headers).json()
>>>>>>> 15457c8d2b3f91e9250ad082455968b4ea355dc3

    def CsvPipeLineTransmit(self, results_lines):
        base_dir = '结果文件'
        if not os.path.isdir(base_dir):
            os.makedirs(base_dir)
        file_path = base_dir + os.sep + 'reposts.csv'
        if not os.path.isfile(file_path):
            is_first_write = 1
        else:
            is_first_write = 0
        if results_lines:
            with open(file_path, 'a', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                if is_first_write:
                    header = [
<<<<<<< HEAD
                        'mid', 'transmit_mid', 'transmit_user_id', 'transmit_user_screen_name', 'transmit_text'
=======
                        'mid', 'transmit_mid', 'transmit_user_id', 'transmit_user_screen_name'
>>>>>>> 15457c8d2b3f91e9250ad082455968b4ea355dc3
                    ]
                    writer.writerow(header)
                for line in results_lines:
                    writer.writerow(line)