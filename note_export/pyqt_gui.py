#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@project: PyCharm
@file: pyqt_gui.py
@author: Shengqiang Zhang
@time: 2022-03-16 21:35:46
@mail: sqzhang77@gmail.com
"""

from wereader import *
from excel_func import *
import sys
import os
import time
from tqdm import tqdm
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
import os
sys.path.append("../tools")
from mysql_tools import *

def get_develop_env():
    develop_env = os.environ["DEVELOP_ENV"]
    return develop_env


# 设置header
HEADERS = {
    'Host': 'i.weread.qq.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}

# 微信读书用户id
USER_VID = 0

def insert_author_info(book,wechat_book_id,type):
    # 插入作者表
    author_name = book[2]
    author_list = select_author(author_name)
    if len(author_list) == 0:
        author_id = insert_author(author_name)
    else:
        author_id = author_list[0].id

    # 修改书籍相关信息
    update_book(wechat_book_id, author_name, book[3], author_id, type)


def insert_book_list(pbar,type):
    for book in pbar:
        wechat_book_id = book[0]
        book_name = book[1]

        # 先判断书籍表中有没有同名的数据，如果没有，就插入到书籍表中
        book_list = select_book(wechat_book_id,book_name)

        if len(book_list) == 0:
            book_id = insert_book(wechat_book_id,book_name)

            # 获取某本书的标签
            tag_list = get_booktags(wechat_book_id, HEADERS)

            # 插入标签数据到数据库
            if len(tag_list) > 0:
                for tag in tag_list:
                    # 先判断标签表中有没有同名的标签，如果没有，就插入到标签表中
                    tag_list = select_tag(tag)
                    if len(tag_list) > 0:
                        tag_id = tag_list[0].id
                    else:
                        tag_id = insert_tag(tag)

                    # 先判断关联表中有没有同名的关联，如果没有，就插入到关联表中
                    book_tag_relation_list = select_book_tag_relation(wechat_book_id, tag_id)
                    if len(book_tag_relation_list) == 0:
                        insert_book_tag_relation(wechat_book_id, book_id, tag_id)
            # 插入作者数据到数据库
            insert_author_info(book, wechat_book_id, type)

            # 失败重试，最大重试次数为4
            for try_count in range(4):
                try:
                    pbar.set_description("正在导出笔记【{}】".format(book_name))

                    # 获取最热划线句子
                    best_notes,item_list = get_bestbookmarks(book[0], HEADERS)
                    # with open(note_dir + book_name + '-best.txt', 'w', encoding='utf-8') as f:
                    #     f.write(best_notes)

                    for item in item_list:
                        wechat_book_id = item['bookId']
                        underline_num = item['totalCount']
                        sentence = item['markText']
                        book_sentence_list = select_book_sentence(sentence,wechat_book_id)
                        if len(book_sentence_list) == 0:
                            book_list = select_book_by_wechat_book_id(wechat_book_id)
                            book_id = book_list[0].id
                            book_name = book_list[0].name
                            insert_book_sentence(sentence,book_id,wechat_book_id,book_name,underline_num, 1)

                    # # 获取自己划线句子
                    # notes = get_bookmarklist(book[0], HEADERS)
                    # with open(note_dir + book_name + '.txt', 'w', encoding='utf-8') as f:
                    #     f.write(notes)

                    # 获取自己的想法
                    # mythought_notes = get_mythought(book[0],HEADERS)
                    # with open(note_dir + book_name + '-mythought.txt', 'w', encoding='utf-8') as f:
                    #     f.write(mythought_notes)

                    # 写入成功后跳出循环，防止重复写入
                    break
                except Exception as e:
                    # 忽略异常，直接重试
                    print(e)
                    pbar.set_description("获取笔记【{}】失败，开始第{}次重试".format(book_name, try_count + 1))

                    # 等待3秒后再重试
                    time.sleep(3)
        else:
            insert_author_info(book, wechat_book_id, type)



class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.DomainCookies = {}

        self.setWindowTitle('微信读书助手') # 设置窗口标题
        self.resize(900, 600) # 设置窗口大小
        self.setWindowFlags(Qt.WindowMinimizeButtonHint) # 禁止最大化按钮
        self.setFixedSize(self.width(), self.height()) # 禁止调整窗口大小

        url = 'https://weread.qq.com/#login' # 目标地址
        self.browser = QWebEngineView() # 实例化浏览器对象

        self.profile = QWebEngineProfile.defaultProfile()
        self.profile.cookieStore().deleteAllCookies() # 初次运行软件时删除所有cookies
        self.profile.cookieStore().cookieAdded.connect(self.onCookieAdd) # cookies增加时触发self.onCookieAdd()函数

        self.browser.loadFinished.connect(self.onLoadFinished) # 网页加载完毕时触发self.onLoadFinished()函数

        self.browser.load(QUrl(url)) # 加载网页
        self.setCentralWidget(self.browser) # 设置中心窗口





    # 网页加载完毕事件
    def onLoadFinished(self):

        global USER_VID
        global HEADERS

        # 获取cookies
        cookies = ['{}={};'.format(key, value) for key,value in self.DomainCookies.items()]
        cookies = ' '.join(cookies)
        # 添加Cookie到header
        HEADERS.update(Cookie=cookies)

        # 判断是否成功登录微信读书
        if login_success(HEADERS):
            print('登录微信读书成功!')

            # 获取用户user_vid
            if 'wr_vid' in self.DomainCookies.keys():
                USER_VID = self.DomainCookies['wr_vid']
                print('用户id:{}'.format(USER_VID))

                # 注入javascript脚本，与网页交互
                self.browser.page().runJavaScript('alert("登录成功！")')

                # 关闭整个qt窗口
                self.close()

        else:
            print('请扫描二维码登录微信读书...')




    # 添加cookies事件
    def onCookieAdd(self, cookie):
        if 'weread.qq.com' in cookie.domain():
            name = cookie.name().data().decode('utf-8')
            value = cookie.value().data().decode('utf-8')
            if name not in self.DomainCookies:
                self.DomainCookies.update({name: value})




    # 窗口关闭事件
    def closeEvent(self, event):
        """
        重写closeEvent方法，实现窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """

        self.setWindowTitle('退出中……')  # 设置窗口标题

        # 关闭软件软件之前删除所有cookies
        # 此代码不可删除，否则下次打开软件会自动加载浏览器中旧的cookies
        self.profile.cookieStore().deleteAllCookies()




if __name__=='__main__':
    app = QApplication(sys.argv) # 创建应用
    window = MainWindow() # 创建主窗口
    window.show() # 显示窗口
    app.exec_() # 运行应用，并监听事件

    # 创建目录
    BASE_ROOT = ''
    env = get_develop_env()
    if env == "test":
        BASE_ROOT = '/home/mocuili/data/enjoy/'
    if env == "prod":
        BASE_ROOT = '/data/enjoy/'
    data_dir = BASE_ROOT+'wechat_export/'
    note_dir = data_dir + '我的笔记/'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if not os.path.exists(note_dir):
        os.makedirs(note_dir)



    books = get_bookshelf(USER_VID, HEADERS) # 获取书架上的书籍
    books_finish_read = books['finishReadBooks']

    books_finish_read = [[book.bookId, book.title, book.author, book.cover] for book in books_finish_read]
    books_recent_read = books['recentBooks']
    books_recent_read = [[book.bookId, book.title, book.author, book.cover] for book in books_recent_read]
    books_all = books['allBooks']
    books_all = [[book.bookId, book.title, book.author, book.cover] for book in books_all]
    write_excel_xls(data_dir + '我的书架.xls', ['已读完的书籍', '最近阅读的书籍', '所有的书籍'], [["ID", "标题", "作者", "封面"], ]) # 写入excel文件
    write_excel_xls_append(data_dir + '我的书架.xls', '已读完的书籍', books_finish_read) # 追加写入excel文件
    write_excel_xls_append(data_dir + '我的书架.xls', '最近阅读的书籍', books_recent_read)  # 追加写入excel文件
    write_excel_xls_append(data_dir + '我的书架.xls', '所有的书籍', books_all)  # 追加写入excel文件

    for index in range(56,72):
        print("==========================index:",str(index))
        maxIdx = 50 * index
        # 心理学类目id:800000,type:1;文学类目id:300000;type:2
        books_all = get_book_by_category(300000, maxIdx, HEADERS)
        type=2

        # 获取【已读完的书籍】的笔记，如果想获取所有书籍的笔记，
        # 请自行更改books_finish_read为books_all
        pbar = tqdm(books_all)

        # 插入书籍，标签，金句数据到数据库
        insert_book_list(pbar,type)


