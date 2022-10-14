# -*- coding: utf-8 -*-
# __author__ = 'SnkrGao'
# __time__ = '2022/9/9 10:39'
import requests
import os
import time
import csv

class parseAttitude():
    def __init__(self, cookie, weibo_id):
        self.cookie = cookie
        self.weibo_id = weibo_id
        self.referer = 'https://m.weibo.cn/detail/' + weibo_id
        self.headers = {
            'Accept':'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'referer': self.referer,
            'cookie': self.cookie,
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Mobile Safari/537.36'
        }

    def SpiderAttitude(self):
        page_num = 1
        # 构造初始转发的url
        initial_url = 'https://m.weibo.cn/api/attitudes/show?id=' + self.weibo_id + '&page=' + str(page_num)
        response = requests.get(initial_url, headers=self.headers).json()
        while response['ok'] == 1:
            transmit_id, transmit_user_id, transmit_user_screen_name = [], [], []
            try:
                results_lines = []
                data_list = response['data']['data']
                if data_list == None:  #可能存在有很多条点赞但只能解析到某一页，response返回的是成功获取数据，但获取到的data中为空值的情况（一般来说最多能获取到50页）
                    break;
                n = len(data_list)
                for i in range(n):
                    data = data_list[i]
                    # transmit_id.append(data['id'])
                    # transmit_user_id.append(data['user']['id'])
                    # transmit_user_screen_name.append(data['user']['screen_name'])
                    results_lines.append((self.weibo_id, data['id'], data['user']['id'], data['user']['screen_name']))
                self.CsvPipeLineAttitude(results_lines)
                time.sleep(2)
                page_num += 1
                initial_url = 'https://m.weibo.cn/api/attitudes/show?id=' + self.weibo_id + '&page=' + str(page_num)
                response = requests.get(initial_url, headers=self.headers).json()
            except Exception as e:
                print(e)

    def CsvPipeLineAttitude(self, results_lines):
        base_dir = '结果文件'
        if not os.path.isdir(base_dir):
            os.makedirs(base_dir)
        file_path = base_dir + os.sep + 'attitudes.csv'
        if not os.path.isfile(file_path):
            is_first_write = 1
        else:
            is_first_write = 0
        if results_lines:
            with open(file_path, 'a', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                if is_first_write:
                    header = [
                        'mid', 'attitude_id', 'attitude_user_id', 'attitude_user_screen_name'
                    ]
                    writer.writerow(header)
                for line in results_lines:
                    writer.writerow(line)