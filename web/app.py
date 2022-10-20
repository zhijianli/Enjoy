from flask import Flask, render_template, request, jsonify
import argparse
import sys
import pandas as pd
import xlrd
from xlutils.copy import copy
import socket

# 判断环境
hostname = socket.gethostname()
if hostname == 'mocuili-Lenovo-Legion-R9000K2021H':
    env = "test"
else:
    env = "prod"

if env == "test":
    sys.path.append("/home/mocuili/github/Enjoy/clip")
if env == "prod":
    sys.path.append("/github/clip")

from video_clip import generate_video

#创建Flask对象app并初始化
app = Flask(__name__)



#通过python装饰器的方法定义路由地址
@app.route("/")
#定义方法 用jinjia2引擎来渲染页面，并返回一个index.html页面
def root():
    return render_template("index.html")

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
@app.route("/submit",methods=["GET", "POST"])
#从这里定义具体的函数 返回值均为json格式
def submit():
    #由于POST、GET获取数据的方式不同，需要使用if语句进行判断
    if request.method == "GET":
        title = request.args.get("title")
        start = request.args.get("start")
        text = request.args.get("text")
        end = request.args.get("end")
        author = request.args.get("author")
        label = request.args.get("label")
        picture = request.args.get("picture")
        music = request.args.get("music")
    if request.method == "POST":
        title = request.form.get("title")
        start = request.form.get("start")
        text = request.form.get("text")
        end = request.form.get("end")
        author = request.form.get("author")
        picture = request.form.get("picture")
        music = request.form.get("music")
        label = request.form.get("label")

    print("title:"+str(title))
    print("start:"+str(start))
    print("text:"+str(text))
    print("end:"+str(end))
    print("author:"+str(author))
    print("picture:"+str(picture))
    print("music:"+str(music))
    print("label:"+str(label))

    num = write_excel(title, start, text, end, author)

    print("＝＝＝＝＝＝＝开始生成视频＝＝＝＝＝＝＝")
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
    args.num = num
    args.env = env
    if label is not None and len(label) > 0:
        args.label = label
    if music is not None and len(music) > 0:
        args.music = music
    if picture is not None and len(picture) > 0:
        args.picture = picture
    print("接受参数：picture：" + str(args.picture))
    print("接受参数：music：" + str(args.music))
    print("接受参数：dubbing：" + str(args.dubbing))
    print("接受参数：num：" + str(args.num))
    print("接受参数：template：" + str(args.template))
    print("接受参数：uploadoss：" + str(args.uploadoss))
    print("接受参数：env：" + str(args.env))
    print("接受参数：label：" + str(args.label))

    generate_video(args)

    #如果获取的数据为空
    # if len(name) == 0 or len(age) ==0:
    #     return {'message':"error!"}
    # else:
    return {'message':"视频生成完毕"}

#定义app在8080端口运行
app.run(host = '0.0.0.0',port=8088)