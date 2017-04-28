# coding: utf8

# @Author: 郭 璞
# @File: login.py                                                                 
# @Time: 2017/4/28                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: CSDN login for returning the same session for backing up the blogs.

import requests
from bs4 import BeautifulSoup
import json

class Login(object):
    """
    Get the same session for blog's backing up. Need the special username and password of your account.
    """
    def __init__(self, username, password):
        if username and password:
            self.username = username
            self.password = password
            # the common headers for this login operation.
            self.headers = {
                'Host': 'passport.csdn.net',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
            }
        else:
            raise Exception('Need Your username and password!')
    def login(self):
        loginurl = 'https://passport.csdn.net/account/login'
        # get the 'token' for webflow
        self.session = requests.Session()
        response = self.session.get(url=loginurl, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Assemble the data for posting operation used in logining.
        self.token = soup.find('input', {'name': 'lt'})['value']

        payload = {
            'username': self.username,
            'password': self.password,
            'lt': self.token,
            'execution': soup.find('input', {'name': 'execution'})['value'],
            '_eventId': 'submit'
        }
        response = self.session.post(url=loginurl, data=payload, headers=self.headers)

        # get the session
        return self.session if response.status_code==200 else None

    def getSource(self, url):
        """
        测试内容， 可删去，(*^__^*) 嘻嘻……
        :param url:
        :return:
        """
        username, id = url.split('/')[3], url.split('/')[-1]
        # print(username, id)
        backupurl = 'http://write.blog.csdn.net/mdeditor/getArticle?id={}&username={}'.format(id, username)
        tempheaders = self.headers
        tempheaders['Referer'] = 'http://write.blog.csdn.net/mdeditor'
        tempheaders['Host'] = 'write.blog.csdn.net'
        tempheaders['X-Requested-With'] = 'XMLHttpRequest'
        response = self.session.get(url=backupurl, headers=tempheaders)
        soup = json.loads(response.text)
        return {
            'title': soup['data']['title'],
            'markdowncontent': soup['data']['markdowncontent'],
        }
