import schedule
import time
import argparse
import sys
import os

sys.path.append(os.path.dirname(sys.path[0]))
from tools.bilibili_open_api import *
from tools.mysql_tools import *

number = 1


# 定义你要周期运行的函数
def job():

   print("刷新令牌定时程序开始执行:"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

   global number

   # 从数据库取最新的refresh_token
   platform_token = select_refresh_token("bilibili")
   r_token = platform_token.refresh_token
   print("r_token", r_token)
   print("number", number)

   # 调用刷新令牌接口
   content = refresh_token(r_token)
   r_token = content['data']['refresh_token']
   access_token = content['data']['access_token']

   # 将更新的refresh_token保存进数据库
   update_platform_token("bilibili", r_token,access_token)

   if number > 5:
       user_info = get_user_info(access_token)
       print("user_info",user_info)

   number = number + 1

   print("刷新令牌定时程序执行结束"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

def start_refresh_access(code):

    schedule.every(1).minutes.do(job)
    print("code", code)
    content = get_access_token(code)
    r_token = content['data']['refresh_token']
    access_token = content['data']['access_token']
    update_platform_token("bilibili", r_token,access_token)

    # 要在这里进行异步编程
    while True:
        schedule.run_pending()  # 运行所有可以运行的任务
        time.sleep(1)


if __name__ == '__main__':

    # 每个小时跑一次
    # schedule.every().day.at("16:39").do(job)
    # schedule.every().hour.do(job)
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--code', type=str, default=None)
    args = parser.parse_args()

    schedule.every(1).minutes.do(job)
    code = args.code
    print("code",code)
    content = get_access_token(code)
    r_token = content['data']['refresh_token']

    while True:
        schedule.run_pending()  # 运行所有可以运行的任务
        time.sleep(1)