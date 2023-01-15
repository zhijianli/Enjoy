from flask import Flask, render_template, request, jsonify
import argparse
import sys
import pandas as pd
import xlrd
from xlutils.copy import copy
import socket
import os
import multiprocessing

# 判断环境
def get_develop_env():
    develop_env = os.environ["DEVELOP_ENV"]
    return develop_env

env = get_develop_env()
book_path = ""
if env == "test":
    book_path = "/home/mocuili/data/enjoy/wechat_export/我的笔记/"
    DATA_ROOT = "/home/mocuili/data/enjoy/"
    CODE_ROOT = "/home/mocuili/github/Enjoy/"
if env == "prod":
    book_path = "/data/enjoy/wechat_export/我的笔记/"
    DATA_ROOT = "/data/enjoy/"
    CODE_ROOT = "/github/"

print("root_path",os.path.dirname(sys.path[0]))
sys.path.append(os.path.dirname(sys.path[0]))

from clip.clause import *
from clip.video_clip import generate_video,preview
from clip.file_operate import get_file_name_list,urllib_download
import tools.aliyun_cutout as aliyun_cutout
from tools.aliyun_oss import put_object_from_file,get_bucket_list
from tools.mysql_tools import *
from tools.my_logging import *
from tools.bilibili_open_api import *
from tools.my_time import *
from timing_program.bilibili_refresh_access import *

refresh_access_process = None

#创建Flask对象app并初始化
app = Flask(__name__)



#通过python装饰器的方法定义路由地址
@app.route("/clip/")
#定义方法 用jinjia2引擎来渲染页面，并返回一个index.html页面
def root():
    return render_template("/content_production/index.html")

@app.route("/videoList/")
#定义方法 用jinjia2引擎来渲染页面，并返回一个index.html页面
def videoList():
    return render_template("/content_production/videoList.html")

@app.route("/")
def mengan():
    return render_template("/official_website/index.html")

@app.route("/about/")
def about():
    return render_template("/official_website/About.html")

@app.route("/news/")
def news():
    return render_template("/official_website/News.html")

@app.route("/newsDetail/")
def newsDetail():
    return render_template("/official_website/news-detail.html")


def write_excel(title,start,text,end,author):
    if env == "test":
        file_path = "/home/mocuili/data/enjoy/text/text.xlsx"
    if env == "prod":
        file_path = "/data/enjoy/text/text.xlsx"
    rb = xlrd.open_workbook(file_path, formatting_info=False)
    rows_num = rb.sheets()[0].nrows

    wb = copy(rb)
    ws = wb.get_sheet(0)

    ws.write(rows_num, 0, title)
    ws.write(rows_num, 1, start)
    ws.write(rows_num, 2, text)
    ws.write(rows_num, 3, end)
    ws.write(rows_num, 4, author)
    wb.save(file_path)

    # 放到excel表中，并且返回num
    num = rows_num - 1
    return num


#app的路由地址"/submit"即为ajax中定义的url地址，采用POST、GET方法均可提交
@app.route("/clip/submit",methods=["GET", "POST"])
#从这里定义具体的函数 返回值均为json格式
def submit():
    if request.method == "POST":
        title = request.form.get("title")
        start = request.form.get("start")
        text = request.form.get("text")
        end = request.form.get("end")
        author = request.form.get("author")
        picture = request.form.get("picture")
        music = request.form.get("music")
        music = music.split("\\")[-1]
        label = request.form.get("label")
        operate = request.form.get("operate")
        font_cover_ratio = request.form.get("font_cover_ratio")
        commentguide = request.form.get("commentguide")

    # 接收参数
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--picture', type=str, default = None) #背景图片
    parser.add_argument('--music', type=str, default= None) #背景音乐
    parser.add_argument('--dubbing', type=int, default= 0) #AI配音
    parser.add_argument('--num', type=int, default= 0) #文字标号
    parser.add_argument('--template', type=int, default=0) #视频制作模板
    parser.add_argument('--uploadoss', type=int, default=0)  #是否上传oss
    parser.add_argument('--env', type=str, default= "test") #环境
    parser.add_argument('--label', type=str, default=None)  # AI配音
    args = parser.parse_args()
    args.template = 1
    args.env = env
    args.commentguide = commentguide
    if label is not None and len(label) > 0:
        args.label = label
    if music is not None and len(music) > 0:
        args.music = music
    if picture is not None and len(picture) > 0:
        args.picture = picture

    # 获取封面字体和封面宽度的比值
    if font_cover_ratio is None:
        args.font_cover_ratio = 10
    else:
        args.font_cover_ratio = font_cover_ratio

    result_message = ""
    if operate == "generateVideo":
        num = insert_video(title, author,end,commentguide, text,
                           "https://enjoy-mocuili.oss-cn-hangzhou.aliyuncs.com/picture/"+picture,
                           music, font_cover_ratio, 124,
                           "描述", label, 0)
        args.num = num
        cover_url,video_url,title,music_file_name,picture_file_name,author,video_time,text = generate_video(args)
        result_message = {'cover_url': cover_url,
                          'video_url': video_url,
                          'title':title,
                          'music_file_name':music_file_name,
                          'picture_file_name':picture_file_name,
                          'author':author,
                          'video_time':video_time,
                          'commentguide':args.commentguide,
                          'text':text}
    elif operate == "preview":
        num = write_excel(title, start, text, end, author)
        args.num = num
        frame_list,title,music_file_name,picture_file_name,author,video_time,text = preview(args)
        result_message = {'frame_list': frame_list,
                          'title':title,
                          'music_file_name':music_file_name,
                          'picture_file_name':picture_file_name,
                          'author':author,
                          'video_time':video_time,
                          'commentguide':args.commentguide,
                          'text':text}

    return result_message

@app.route("/clip/get_search_condition",methods=["GET"])
def get_search_condition():
    # file_name_list = get_file_name_list(book_path)
    # 获取书籍列表
    book_list = select_book_list()
    book_name_list = []
    book_wechar_id_list = []
    for book in book_list:
        book_name_list.append(book.name)
        book_wechar_id_list.append(book.wechat_book_id)

    # 获取标签列表
    tag_name_list = []
    tag_id_list = []
    tag_list = select_tag_list()
    for tag in tag_list:
        tag_id_list.append(tag.id)
        tag_name_list.append(tag.name)

    # 获取作者列表
    author_id_list = []
    author_name_list = []
    author_list = select_author_list()
    for author in author_list:
        author_id_list.append(author.id)
        author_name_list.append(author.name)

    return {'book_name_list': book_name_list,
            'book_wechar_id_list':book_wechar_id_list,
            'tag_id_list':tag_id_list,
            'tag_name_list':tag_name_list,
            'author_id_list':author_id_list,
            'author_name_list':author_name_list}

@app.route("/clip/get_content_by_book",methods=["GET"])
def get_content_by_book():
    # file_object = open(book_path+book_name)
    # try:
    #     book_content = file_object.read()
    # finally:
    #     file_object.close()
    wechar_book_id = request.args.get("wechar_book_id")
    book_sentence_list = select_book_sentence_by_wechat_id(wechar_book_id)
    book_content = ''
    for book_sentence in book_sentence_list:
        book_content = book_content + book_sentence.sentence + "－－《" + book_sentence.book_name + "》" + "划线数：" + str(book_sentence.underline_num) + '\n\n'
    return {'message': book_content}


@app.route("/clip/book_search",methods=["GET"])
def book_search():
    key_words = request.args.get("key_words")
    wechat_book_id = request.args.get("wechat_book_id")
    book_sentence_list = select_book_sentence_by_condition(key_words,wechat_book_id)
    book_content = ''
    for book_sentence in book_sentence_list:
        book_content = book_content + book_sentence.sentence + "－－《" + book_sentence.book_name + "》" + "划线数：" + str(book_sentence.underline_num) + '\n\n'
    return {'message': book_content}

@app.route("/clip/book_search_list",methods=["GET"])
def book_search_list():
    key_words = request.args.get("key_words")
    wechat_book_id = request.args.get("wechat_book_id")
    author_id = request.args.get("author_id")
    tag_id = request.args.get("tag_id")
    type = request.args.get("type")
    book_id_list = []
    is_no_book=False

    current_time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # 筛选出相应标签的book_id
    if len(tag_id)>0:
        book_tag_relation_list = select_relation_by_tag_id(tag_id)
        if len(book_tag_relation_list)>0:
            for relation in book_tag_relation_list:
                book_id_list.append(relation.book_id)
        else:
            is_no_book = True
    current_time2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 筛选出相应类型和作者的book_id
    if is_no_book == False and (len(author_id)>0 or len(type)>0):
        book_list = select_book_by_condition(type,author_id,book_id_list)
        book_id_list = []
        if len(book_list)>0:
            for book in book_list:
                book_id_list.append(book.id)
        else:
            is_no_book = True
    current_time3 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 筛选出金句列表
    book_sentence_str_list = []
    book_name_list = []
    underline_num_list = []
    if is_no_book is False:
        book_sentence_list = select_book_sentence_by_condition(key_words,wechat_book_id,book_id_list)
        for book_sentence in book_sentence_list:
            sentence = book_sentence.sentence
            # 做断句
            sentence = sentence_break(sentence)
            book_sentence_str_list.append(sentence)
            book_name_list.append(book_sentence.author_name+" 《" + str(book_sentence.book_name) + "》")
            underline_num_list.append(book_sentence.underline_num)
    current_time4 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    # info_log("time",current_time1,current_time2,current_time3,current_time4)
    return {'book_sentence_str_list': book_sentence_str_list,
            'book_name_list': book_name_list,
            'underline_num_list': underline_num_list}

@app.route("/clip/cutout",methods=["GET"])
def cutout():
    avatarUrl = request.args.get("avatarUrl")
    author = request.args.get("author")

    result_url = aliyun_cutout.cutout(avatarUrl)
    local_path = DATA_ROOT+"avatar/"+author+".jpg"
    # 下载到本地
    urllib_download(result_url,local_path)

    # 上传到阿里云
    put_object_from_file("avatar/" + author+".jpg",local_path)

    return {'result_url': result_url}

@app.route("/clip/get_picture_list",methods=["GET"])
def get_picture_list():

    # 获取阿里云oss背景图片链接list
    picture_list = get_bucket_list(".jpg")

    return {'picture_list': picture_list}



@app.route("/clip/save_picture",methods=["POST"])
def save_picture():
    picture_url = request.form.get("picture_url")
    picture_name = picture_url.split("\\")[-1]
    put_object_from_file("picture/" + picture_name, picture_url)
    return {'result_message': "success"}

line_number = [0] #存放当前日志行数
# 定义接口把处理日志并返回到前端
@app.route('/clip/get_log',methods=['GET','POST'])
def get_log():
    log_data = red_logs() # 获取日志
    # 判断如果此次获取日志行数减去上一次获取日志行数大于0，代表获取到新的日志
    if len(log_data) - line_number[0] > 0:
        log_type = 2 # 当前获取到日志
        log_difference = len(log_data) - line_number[0] # 计算获取到少行新日志
        log_list = [] # 存放获取到的新日志
        # 遍历获取到的新日志存放到log_list中
        for i in range(log_difference):
            log_i = log_data[-(i+1)].decode('utf-8') # 遍历每一条日志并解码
            log_list.insert(0,log_i) # 将获取的日志存放log_list中
    else:
        log_type = 3
        log_list = ''
    # 已字典形式返回前端
    _log = {
        'log_type' : log_type,
        'log_list' : log_list
    }
    line_number.pop() # 删除上一次获取行数
    line_number.append(len(log_data)) # 添加此次获取行数
    return {'_log': _log}


@app.route('/videoList/bilibili_video_contribute',methods=['GET'])
def bilibili_video_contribute():

    video_id = request.args.get("video_id")
    video = select_video(video_id)
    status = video.status
    datetime = request.args.get("datetime")

    # 判断一下稿件状态
    if status == 2:  # 如果状态是＂已投稿＂则返回已投稿信息，
        return {'message': "投稿已投递，请勿重复投稿"}
    elif status == 1:  # 如果状态是＂定时投稿＂，则返回定时投稿信息
        return {'message': "投稿已定时，请勿重复投稿，定时时间为："+datetime}
    elif status == 0:
        if datetime is None or len(datetime) == 0: # 如果状态是＂未投稿＂并且时间为空，则立即投稿
            message = contribute_process(video)
            return {'message': "恭喜，投稿成功！！！"}
        if isVaildDate(datetime):# 如果状态是＂未投稿＂并且时间符合格式，则不立即投稿，等待定时程序投稿
            update_video_contribute_time_and_status(video_id,datetime,1)
            return {'message': "稿件已完成定时，时间为："+datetime}
        else:
            return {'message': "时间格式有问题，请检查"}
    else:
        return {'message': "稿件状态有问题，请检查稿件状态"}

    return {'message': "恭喜，投稿成功！！！"}


@app.route('/clip/bilibili_code',methods=['GET'])
def bilibili_code():
    code = request.args.get("code")

    # # 获取token
    # content = get_access_token(code)
    # access_token = content['data']['access_token']

    return {'message': code}

@app.route('/clip/bilibili_refresh_access',methods=['GET'])
def bilibili_refresh_access():
    global refresh_access_process

    code = request.args.get("code")

    print("refresh_access_process",refresh_access_process)
    # 杀死原先的刷新令牌程序
    if refresh_access_process is not None and refresh_access_process.is_alive:
        refresh_access_process.terminate()
        refresh_access_process.join()
        print('stop process')

    # 启动刷新令牌程序
    refresh_access_process = multiprocessing.Process(target=start_refresh_access(code))
    refresh_access_process.start()
    # os.system("python3 /github/timing_program/bilibili_refresh_access.py --code %s" % code)

    return {'message': code}


@app.route('/videoList/get_video_list',methods=['GET'])
def get_video_list():

    video_list = select_video_list()
    video_id_list = []
    video_title_list = []
    video_cover_url_list = []
    video_bgm_list = []
    video_subtitle_list = []
    video_comment_guide_list = []
    video_status_list = []
    video_contribute_time_list = []
    for video in video_list:
        video_id_list.append(video.id)
        video_title_list.append(video.title)
        video_cover_url_list.append(video.cover_url)
        video_bgm_list.append(video.bgm_name)
        video_subtitle_list.append(video.subtitle)
        video_comment_guide_list.append(video.comment_guide)
        if video.status == 0:
            video_status_list.append("未投稿")
        elif video.status == 1:
            video_status_list.append("已定时")
        elif video.status == 2:
            video_status_list.append("已投稿")
        video_contribute_time_list.append(video.contribute_time)

    return {'video_id_list':video_id_list,
            'video_title_list': video_title_list,
            'video_cover_url_list' : video_cover_url_list,
            'video_bgm_list' : video_bgm_list,
            'video_subtitle_list' : video_subtitle_list,
            'video_comment_guide_list':video_comment_guide_list,
            'video_status_list':video_status_list,
            'video_contribute_time_list':video_contribute_time_list}


if env == "test":
    app.run(host='0.0.0.0', port=8088)
if env == "prod":
    app.run(host = '0.0.0.0',port=80)