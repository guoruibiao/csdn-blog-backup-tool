# coding: utf8

# @Author: 郭 璞
# @File: Main.py                                                                 
# @Time: 2017/4/28                                   
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: The entrance of this blog backup tool.

from csdnbackup.login import Login
from csdnbackup.backup import Backup
from csdnbackup.blogscan import BlogScanner

import getpass
username = input('Please input your account name: ')
password = getpass.getpass(prompt='Please type your own account password: ')
loginer = Login(username=username, password=password)
session = loginer.login()

scanner = BlogScanner(username)
links = scanner.scan()

for link in links:
    backupper = Backup(session=session, backupurl=link)
    backupper.backup(outputpath='./')
