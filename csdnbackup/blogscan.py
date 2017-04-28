# coding: utf8

# @Author: 郭 璞
# @File: blogscan.py                                                                 
# @Time: 2017/4/28                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: Scan the domain of your blog domain, get the all links of your blogs.
import requests
from bs4 import BeautifulSoup
import re

class BlogScanner(object):
    """
    Scan for all blogs
    """
    def __init__(self, domain):
        self.username = domain
        self.rooturl = 'http://blog.csdn.net'
        self.bloglinks = []
        self.headers = {
            'Host': 'blog.csdn.net',
            'Upgrade - Insecure - Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
        }

    def scan(self):
        # get the page count
        response = requests.get(url=self.rooturl+"/"+self.username, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        pagecontainer = soup.find('div', {'class': 'pagelist'})
        pages = re.findall(re.compile('(\d+)'), pagecontainer.find('span').get_text())[-1]

        # construnct the blog list. Likes: http://blog.csdn.net/Marksinoberg/article/list/2
        for index in range(1, int(pages)+1):
            # get the blog link of each list page
            listurl = 'http://blog.csdn.net/{}/article/list/{}'.format(self.username, str(index))
            response = requests.get(url=listurl, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            try:
                alinks = soup.find_all('span', {'class': 'link_title'})
                # print(alinks)
                for alink in alinks:
                    link = alink.find('a').attrs['href']
                    link = self.rooturl +link
                    self.bloglinks.append(link)
            except Exception as e:
                print('出现了点意外！\n'+e)
                continue

        return self.bloglinks



