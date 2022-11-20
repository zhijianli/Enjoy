#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
@project: PyCharm
@file: wereader.py
@author: Shengqiang Zhang
@time: 2022-03-16 22:30:52
@mail: sqzhang77@gmail.com
"""

"""
@origin: https://github.com/arry-lee/wereader
@author: arry-lee
@annotation: modified from arry-lee
"""

from collections import namedtuple, defaultdict
from operator import itemgetter
from itertools import chain

import requests
import json
import clipboard
import urllib3

hotmarks_number = {'pre': "`",   'suf': "`  "}#热门标注标注人数前后缀
# 禁用安全警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 书籍信息
Book = namedtuple('Book', ['bookId', 'title', 'author', 'cover'])



def get_bookmarklist(bookId, headers):
    """获取某本书的笔记返回md文本"""
    url = "https://i.weread.qq.com/book/bookmarklist"
    params = dict(bookId=bookId)
    r = requests.get(url, params=params, headers=headers, verify=False)

    if r.ok:
        data = r.json()
        # clipboard.copy(json.dumps(data, indent=4, sort_keys=True))
    else:
        raise Exception(r.text)
    chapters = {c['chapterUid']: c['title'] for c in data['chapters']}
    contents = defaultdict(list)

    for item in sorted(data['updated'], key=lambda x: x['chapterUid']):
        # for item in data['updated']:
        chapter = item['chapterUid']
        text = item['markText']
        create_time = item["createTime"]
        start = int(item['range'].split('-')[0])
        contents[chapter].append((start, text))

    chapters_map = {title: level for level, title in get_chapters(int(bookId), headers)}
    res = ''
    for c in sorted(chapters.keys()):
        title = chapters[c]
        res += '#' * chapters_map[title] + ' ' + title + '\n'
        for start, text in sorted(contents[c], key=lambda e: e[0]):
            res += '> ' + text.strip() + '\n\n'
        res += '\n'

    return res


def get_bestbookmarks(bookId, headers):
    """获取书籍的热门划线,返回文本"""
    url = "https://i.weread.qq.com/book/bestbookmarks"
    params = dict(bookId=bookId)
    r = requests.get(url, params=params, headers=headers, verify=False)
    if r.ok:
        data = r.json()
        # clipboard.copy(json.dumps(data, indent=4, sort_keys=True))
    else:
        raise Exception(r.text)

    if 'chapters' not in data:
        return ''

    chapters = {c['chapterUid']: c['title'] for c in data['chapters']}

    contents = defaultdict(list)

    for item in data['items']:
        chapter = item['chapterUid']
        text = item['markText']
        text_number = set_hotmarks_number(item['totalCount'])
        contents[chapter].append(text_number + text)

    chapters_map = {title: level for level, title in get_chapters(int(bookId),headers)}
    res = ''
    for c in chapters:
        title = chapters[c]
        res += '#' * chapters_map[title] + ' ' + title + '\n'
        for text in contents[c]:
            res += '> ' + text.strip() + '\n\n'
        res += '\n'
    return res,data['items']

def set_hotmarks_number(number):
    global hotmarks_number
    return hotmarks_number['pre'] + str(number) + hotmarks_number['suf']

"""
(按顺序)获取书中的所有个人想法(Markdown格式,含原文,标题分级,想法前后缀)
"""
def get_mythought(bookId,HEADERS):
    res = ''
    """获取数据"""
    if '_' in bookId:
        url = 'https://i.weread.qq.com/review/list?listtype=6&mine=1&bookId=' + bookId + '&synckey=0&listmode=0'
        data = request_data(url,HEADERS)
        print('公众号暂时不支持获取想法')
        return ''
    else:
        url = "https://i.weread.qq.com/review/list?bookId=" + bookId + "&listType=11&mine=1&synckey=0&listMode=0"
        data = request_data(url,HEADERS)
        """ print(data)
        return """
    """遍历所有想法并添加到字典储存起来
    thoughts = {30: {7694: '...',122:'...'}, 16: {422: '...',}, 12: {788: '...',}}
    """
    thoughts = defaultdict(dict)
    MAX = 1000000000
    for item in data['reviews']:
        # 获取想法所在章节id
        chapterUid = item['review']['chapterUid']
        # 获取原文内容
        abstract = item['review']['abstract']
        # 获取想法
        text = item['review']['content']
        # 获取想法开始位置
        try:
            text_positon = int(item['review']['range'].split('-')[0])
        except:
            # 处理在章末添加想法的情况(将位置设置为一个很大的值)
            text_positon = MAX + int(item['review']['createTime'])
        # 以位置为键，以标注为值添加到字典中,获得{chapterUid:{text_positon:"text分开想法和原文内容abstract"}}
        thoughts[chapterUid][text_positon] = text + '分开想法和原文内容' + abstract

    """章节内想法按range排序
    thoughts_sorted_range = 
    {30: [(7694, '....')], 16: [(422, '...')], 12: [(788, '...')]}
    """
    thoughts_sorted_range = defaultdict(list)
    # 每一章内的想法按想法位置排序
    for chapterUid in thoughts.keys():
        thoughts_sorted_range[chapterUid] = sorted(thoughts[chapterUid].items())

    """章节按id排序
    sorted_thoughts = 
    [(12, [(788, '...')]), (16, [(422, '...')]), (30, [(7694, '...')])]
    """
    sorted_thoughts = sorted(thoughts_sorted_range.items())

    """获取包含目录级别的目录数据"""
    # 获取包含目录级别的全书目录[(chapterUid,level,'title')]
    sorted_chapters = get_sorted_chapters(bookId,HEADERS)
    # 去除没有想法的目录项
    d_sorted_chapters = []
    for chapter in sorted_chapters:
        if chapter[0] in thoughts_sorted_range.keys():
            d_sorted_chapters.append(chapter)

    """生成想法"""
    for i in range(len(sorted_thoughts)):
        counter = 1
        res += set_chapter_level(d_sorted_chapters[i][1]) + d_sorted_chapters[i][2] + '\n\n'
        for thought in sorted_thoughts[i][1]:
            text_and_abstract = thought[1].split('分开想法和原文内容')
            # 如果为章末发布的标注（不包含 abstract 的标注）
            if text_and_abstract[1] == '':
                text_and_abstract[1] = "章末想法" + str(counter)
                counter = counter + 1
            res += text_and_abstract[1] + '\n\n' + set_thought_style(text_and_abstract[0]) + '\n\n'
    if res.strip() == '':
        print('无想法')
    return res

def set_thought_style(text):
    global thought_style
    return thought_style['pre'] + text + thought_style['suf']

def set_chapter_level(level):
    global level1,level2,level3
    if level == 1:
        return level1
    elif level == 2:
        return level2
    elif level == 3:
        return level3


"""
(按顺序)获取书中的章节：
[(1, 1, '封面'), (2, 1, '版权信息'), (3, 1, '数字版权声明'), (4, 1, '版权声明'), (5, 1, '献给'), (6, 1, '前言'), (7, 1, '致谢')]
"""
def get_sorted_chapters(bookId,headers):
    if '_' in bookId:
        print('公众号不支持输出目录')
        return ''
    url = "https://i.weread.qq.com/book/chapterInfos?" + "bookIds=" + bookId + "&synckeys=0"
    data = request_data(url,headers)
    chapters = []
    #遍历章节,章节在数据中是按顺序排列的，所以不需要另外排列
    for item in data['data'][0]['updated']:
        #判断item是否包含level属性。
        try:
            chapters.append((item['chapterUid'],item['level'],item['title']))
        except:
            chapters.append((item['chapterUid'],1,item['title']))
    """chapters = [(1, 1, '封面'), (2, 1, '版权信息'), (3, 1, '数字版权声明'), (4, 1, '版权声明'), (5, 1, '献给'), (6, 1, '前言'), (7, 1, '致谢')]"""
    return chapters


def get_chapters(bookId, headers):
    """获取书的目录"""
    url = "https://i.weread.qq.com/book/chapterInfos"
    data = '{"bookIds":["%d"],"synckeys":[0]}' % bookId

    r = requests.post(url, data=data, headers=headers, verify=False)

    if r.ok:
        data = r.json()
        clipboard.copy(json.dumps(data, indent=4, sort_keys=True))
    else:
        raise Exception(r.text)

    chapters = []
    for item in data['data'][0]['updated']:
        if 'anchors' in item:
            chapters.append((item.get('level', 1), item['title']))
            for ac in item['anchors']:
                chapters.append((ac['level'], ac['title']))

        elif 'level' in item:
            chapters.append((item.get('level', 1), item['title']))

        else:
            chapters.append((1, item['title']))

    return chapters


def get_bookinfo(bookId, headers):
    """获取书的详情"""
    url = "https://i.weread.qq.com/book/info"
    params = dict(bookId=bookId)
    r = requests.get(url, params=params, headers=headers, verify=False)

    if r.ok:
        data = r.json()
    else:
        raise Exception(r.text)
    return data

def get_booktags(bookId, headers):
    """获取书的详情"""
    url = "https://i.weread.qq.com/book/detailinfo"
    params = dict(bookId=bookId,
                  count="3, 0, 1",
                  maxidx="0, 0, 0",
                  listtypes="1, 6, 10",
                  synckey="1668837609, 1668841022, 1668841022")

    r = requests.get(url, params=params, headers=headers, verify=False)
    tag_list = []
    if r.ok:
        data = r.json()
        tags = data['booktags']['tags']
        if len(tags) > 0:
            for tag in tags:
                tag_list.append(tag['tag'])

    else:
        raise Exception(r.text)
    return tag_list



def get_bookshelf(userVid, headers):
    """获取书架上所有书"""
    url = "https://i.weread.qq.com/shelf/friendCommon"
    params = dict(userVid=userVid)
    r = requests.get(url, params=params, headers=headers, verify=False)
    if r.ok:
        data = r.json()
    else:
        raise Exception(r.text)

    books_finish_read = set() # 已读完的书籍
    books_recent_read = set() # 最近阅读的书籍
    books_all = set() # 书架上的所有书籍

    for book in data['finishReadBooks']:
        if ('bookId' not in book.keys()) or (not book['bookId'].isdigit()):  # 过滤公众号
            continue
        b = Book(book['bookId'], book['title'], book['author'], book['cover'])
        books_finish_read.add(b)
    books_finish_read = list(books_finish_read)
    books_finish_read.sort(key=itemgetter(-1)) # operator.itemgetter(-1)指的是获取对象的最后一个域的值，即以category进行排序



    for book in data['recentBooks']:
        if ('bookId' not in book.keys()) or (not book['bookId'].isdigit()): # 过滤公众号
            continue
        b = Book(book['bookId'], book['title'], book['author'], book['cover'])
        books_recent_read.add(b)
    books_recent_read = list(books_recent_read)
    books_recent_read.sort(key=itemgetter(-1)) # operator.itemgetter(-1)指的是获取对象的最后一个域的值，即以category进行排序


    books_all = books_finish_read + books_recent_read

    return dict(finishReadBooks=books_finish_read, recentBooks=books_recent_read, allBooks=books_all)


def get_notebooklist(headers):
    """获取笔记书单"""
    url = "https://i.weread.qq.com/user/notebooks"
    r = requests.get(url, headers=headers, verify=False)

    if r.ok:
        data = r.json()
    else:
        raise Exception(r.text)
    books = []
    for b in data['books']:
        book = b['book']
        b = Book(book['bookId'], book['title'], book['author'], book['cover'])
        books.append(b)
    books.sort(key=itemgetter(-1))
    return books

"""由url请求数据"""
def request_data(url,headers):
    r = requests.get(url,headers=headers,verify=False)
    if r.ok:
        data = r.json()
    else:
        raise Exception(r.text)
    return data

def login_success(headers):
    """判断是否登录成功"""
    url = "https://i.weread.qq.com/user/notebooks"
    r = requests.get(url,headers=headers,verify=False)

    if r.ok:
        return True
    else:
        return False

"""根据类目id获取书的目录"""
def get_book_by_category(categoryId,maxIdx,headers):

    url = "https://i.weread.qq.com/category/data"
    params = dict(wordcount_begin=0,
                  synckey=0,
                  maxIdx=maxIdx,
                  count=50,
                  finish=0,
                  sort=1,
                  wordcount_end=0,
                  paytype=0,
                  categoryId=categoryId)

    r = requests.get(url, params=params, headers=headers, verify=False)
    book_list = []
    if r.ok:
        data = r.json()
        books = data['books']
        if len(books) > 0:
            for book in books:
                bookInfo = book['bookInfo']
                book_info_list = [bookInfo['bookId'],bookInfo['title'],bookInfo['author'],bookInfo['cover']]
                book_list.append(book_info_list)
    else:
        raise Exception(r.text)
    return book_list



if __name__ == "__main__":
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

    data = get_book_by_category(800000,10,HEADERS)
    print(data)