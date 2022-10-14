# -*- coding: utf-8 -*-
# __author__ = 'SnkrGao'
# __time__ = '2022/9/9 11:04'
import re
import requests
import os
import time
import csv

class parseComments():
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

    def main(self):
        page_num = 1

        # 构造起始地址
        start_url = f'https://m.weibo.cn/comments/hotflow?id={self.weibo_id}&mid={self.weibo_id}&max_id_type=0'
        response = requests.get(start_url, headers=self.headers).json()
        # print(response)

        # 提取翻页的max_id
        max_id = response['data']['max_id']
        # 提取翻页的max_id_type
        max_id_type = response['data']['max_id_type']

        # 构造GET的请求参数
        data = {
            'id': self.weibo_id,
            'mid': self.weibo_id,
            'max_id': max_id,
            'max_id_type': max_id_type
        }

        # 解析评论内容
        self.parse_response_data(response, page_num)
        time.sleep(10)
        page_num += 1

        while max_id != 0:
            new_url = 'https://m.weibo.cn/comments/hotflow?'
            new_response = requests.get(new_url, headers=self.headers, params=data).json()
            max_id = new_response['data']['max_id']
            # 提取翻页的max_id_type
            max_id_type = new_response['data']['max_id_type']
            # print(max_id, max_id_type)

            # 构造GET的请求参数
            data = {
                'id': self.weibo_id,
                'mid': self.weibo_id,
                'max_id': max_id,
                'max_id_type': max_id_type
            }
            self.parse_response_data(new_response, page_num)
            page_num += 1

    def parse_response_data(self, response, page_num):
        # 从响应中解析评论内容

        # 提取出评论列表
        data_list = response['data']['data']
        # print(data_list)
        n = len(data_list)
        # print(n)
        results_lines = []
        results = []
        for i in range(n):
            try:
                # 评论id
                comment_id = data_list[i]['mid']
                texts = data_list[i]['text']
                # print(texts)
                # sub替换掉标签内容
                alts = ''.join(re.findall(r'alt=(.*?) ', texts))
                pic_urls = ''.join(re.findall(r'src=(.*?) ', texts))
                texts = re.sub("<span.*?</span>", alts, texts)  # 需要替换的内容，替换之后的内容，替换对象
                # print(texts)
                # 评论用户的id
                user_id = data_list[i]['user']['id']
                # 用户名
                screen_names = data_list[i]['user']['screen_name']
                # 是否有二级评论
                has_comments = False
                # secondary_comments = data_list[i]['comments']
                # if secondary_comments:
                #     has_comments = True
                secondary_comments_num = data_list[i]['total_number']
                if secondary_comments_num !=0 :
                    has_comments = True
                results_lines.append(
                    (self.weibo_id, comment_id, user_id, screen_names, texts, pic_urls, has_comments, secondary_comments_num))
                print(comment_id, texts, pic_urls, user_id, screen_names, has_comments, secondary_comments_num)

                # 判断是否有二级评论，若有则解析二级评论的内容
                if has_comments:
                    secondary_page_num = 1
                    # 构造评论详情的url
                    comments_url = f'https://m.weibo.cn/comments/hotFlowChild?cid={comment_id}&max_id=0&max_id_type=0'
                    comments_detail_response = requests.get(comments_url, headers=self.headers).json()
                    # print(comments_detail_response)

                    # 提取翻页的max_id
                    max_id = comments_detail_response['max_id']
                    # 提取翻页的max_id_type
                    max_id_type = comments_detail_response['max_id_type']

                    # 构造GET的请求参数
                    data = {
                        'cid': comment_id,
                        'max_id': max_id,
                        'max_id_type': max_id_type
                    }

                    res = self.parse_secondary_comments(comment_id, comments_detail_response, secondary_page_num,
                                                        results_lines)
                    time.sleep(10)
                    secondary_page_num += 1

                    while max_id != 0:
                        new_comments_url = 'https://m.weibo.cn/comments/hotFlowChild?'
                        new_comments_response = requests.get(new_comments_url, headers=self.headers,
                                                             params=data).json()

                        max_id = new_comments_response['max_id']
                        # 提取翻页的max_id_type
                        max_id_type = new_comments_response['max_id_type']
                        # print(max_id, max_id_type)

                        # 构造GET的请求参数
                        data = {
                            'cid': comment_id,
                            'max_id': max_id,
                            'max_id_type': max_id_type
                        }

                        res = self.parse_secondary_comments(comment_id, new_comments_response, secondary_page_num,
                                                            results_lines)
                        secondary_page_num += 1
                else:
                    self.CsvPipeLineComment(results_lines)
            except Exception as e:
                print(e)

            print()
            results_lines.clear()
        # self.CsvPipeLineComment(results)
        print('*******************************************************************************************')
        print()
        print(f'*****第{page_num}页评论打印完成*****')

    def CsvPipeLineComment(self, results_lines):
        base_dir = '结果文件'
        if not os.path.isdir(base_dir):
            os.makedirs(base_dir)
        file_path = base_dir + os.sep + 'comments.csv'
        if not os.path.isfile(file_path):
            is_first_write = 1
        else:
            is_first_write = 0
        if results_lines:
            with open(file_path, 'a', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f)
                if is_first_write:
                    header = [
                        'mid', 'comment_mid', 'comment_user_id', 'comment_user_screen_name', 'comment_content',
                        'comment_pic_urls', 'has_comments', 'secondary_comments_num',
                        'secondary_comment_mid', 'secondary_comment_user_id', 'secondary_comment_screen_names',
                        'secondary_comment_content', 'secondary_comment_pic_urls'
                    ]
                    writer.writerow(header)
                for line in results_lines:
                    writer.writerow(line)

    def parse_secondary_comments(self, comment_id, comments_detail_response, secondary_page_num, results_lines):
        # 提取评论列表
        comments_list = comments_detail_response['data']
        # print(comments_list)
        n = len(comments_list)
        # print(n)

        comments_lines = []
        res = []
        print(f'*****开始打印{comment_id}的第{secondary_page_num}页二级评论*****')
        for i in range(n):
            # 二级评论id
            secondary_comment_id = comments_list[i]['mid']
            secondary_comment_texts = comments_list[i]['text']
            # print(secondary_comment_texts)
            # sub替换掉标签内容
            secondary_comments_alts = ''.join(re.findall(r'alt=(.*?) ', secondary_comment_texts))
            secondary_comments_pic_urls = ''.join(re.findall(r'src=(.*?) ', secondary_comment_texts))
            secondary_comment_texts = re.sub("回复.*?</a>:", '', secondary_comment_texts)
            secondary_comment_texts = re.sub("<span.*?</span>", secondary_comments_alts,
                                             secondary_comment_texts)  # 需要替换的内容，替换之后的内容，替换对象
            # print(secondary_comment_texts)
            # 二级评论用户的id
            secondary_comment_user_id = comments_list[i]['user']['id']
            # 用户名
            secondary_comment_screen_names = comments_list[i]['user']['screen_name']

            comments_lines.append((secondary_comment_id, secondary_comment_user_id, secondary_comment_screen_names,
                                   secondary_comment_texts, secondary_comments_pic_urls))
            for i, j in zip(results_lines, comments_lines):
                res.append(i + j)
            print(res)
            comments_lines.clear()
            print(secondary_comment_id, secondary_comment_texts, secondary_comment_user_id,
                  secondary_comment_screen_names)
            print()
        self.CsvPipeLineComment(res)
        print(f'*****{comment_id}的第{secondary_page_num}页二级评论打印完成*****')
        return res