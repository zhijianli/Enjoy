import schedule
import time
import argparse
from clip.video_clip import generate_video
from clip.file_operate import copy_file

def print_hi(name):
    print(f'Hi, {name}')

# 定义你要周期运行的函数
def job():

    for i in range(3):
        # 获取内容


        # 生成视频
        print("＝＝＝＝＝＝＝开始生成第"+str(i+1)+"个视频＝＝＝＝＝＝＝")
        parser = argparse.ArgumentParser(description='manual to this script')
        parser.add_argument('--picture', type=str, default = None)
        parser.add_argument('--music', type=str, default= None)
        parser.add_argument('--dubbing', type=int, default= 1)
        parser.add_argument('--num', type=int, default= 0)
        args = parser.parse_args()
        print("接受参数：picture：" + str(args.picture))
        print("接受参数：music：" + str(args.music))
        print("接受参数：dubbing：" + str(args.dubbing))
        print("接受参数：num：" + str(args.num))

        generate_video(args)
        print("＝＝＝＝＝＝＝生成第"+str(i+1)+"个视频结束＝＝＝＝＝＝＝")
    copy_file()

if __name__ == '__main__':

    # # 每天定时早上8点生成3个视频
    # schedule.every().day.at("16:39").do(job)  # 每天在 10:30 时间点运行 job 函数
    #
    # while True:
    #     schedule.run_pending()  # 运行所有可以运行的任务
    #     time.sleep(1)
    copy_file()