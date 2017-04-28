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

loginer = Login(username='marksinoberg', password='PRCstylewarmup')
session = loginer.login()

scanner = BlogScanner('marksinoberg')
links = scanner.scan()

for link in links:
    backupper = Backup(session=session, backupurl=link)
    backupper.backup(outputpath='./')
