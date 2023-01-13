import schedule
import time
import argparse
from clip.video_clip import generate_video
from clip.file_operate import copy_file
from tools.mysql_tools import *
from tools.bilibili_open_api import *

r_token = ''
number = 0

def print_hi(name):
    print(f'Hi, {name}')

# 定义你要周期运行的函数
def job():

   print("投稿定时程序开始执行:"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

   # time.sleep(2)
   # video_list = select_video_list()
   # for video in video_list:
   #     status = video.status
   #     if status == 1: #表明视频状态是在定时投稿中
   #         print(video.title)
   global r_token
   global number
   content = refresh_token(r_token)
   r_token = content['data']['refresh_token']

   number = number + 1
   print("number",number)
   if number > 5:
       access_token = content['data']['access_token']
       user_info = get_user_info(access_token)
       print("user_info",user_info)

   print("投稿定时程序执行结束"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

if __name__ == '__main__':

    # 每个小时跑一次
    # schedule.every().day.at("16:39").do(job)
    # schedule.every().hour.do(job)
    schedule.every(1).minutes.do(job())
    code = ''
    content = get_access_token(code)
    r_token = content['data']['refresh_token']

    while True:
        schedule.run_pending()  # 运行所有可以运行的任务
        time.sleep(1)