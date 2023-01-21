import schedule
import time
import argparse
import sys
import os

sys.path.append(os.path.dirname(sys.path[0]))
from tools.bilibili_open_api import *
from tools.mysql_tools import *


# 定义你要周期运行的函数
def job():

   print("生成视频内容定时程序开始执行:"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

   print("")

   print("生成视频内容定时程序执行结束"+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))




if __name__ == '__main__':

    print("生成视频内容定时程序启动成功：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    # 每个小时跑一次
    # schedule.every(1).minutes.do(job)
    schedule.every().hour.do(job)

    while True:
        schedule.run_pending()  # 运行所有可以运行的任务
        time.sleep(1)