import pandas as pd
import sys
import time
import argparse
import numpy as np
import subprocess
from moviepy.editor import *
from clause import cut_sent,sub
from file_operate import get_file_list
from get_audio_time import get_duration_wav
from moviepy.video.tools.drawing import color_gradient
from moviepy.video.tools.drawing import color_split


# 接收参数
parser = argparse.ArgumentParser(description='manual to this script')
parser.add_argument('--picture', type=str, default = None)
parser.add_argument('--music', type=str, default= None)
args = parser.parse_args()
print("接受参数：picture：" + str(args.picture))
print("接受参数：music：" + str(args.music))

# 加载text数据
num = 4
# DATA_ROOT = "/home/mocuili/data/enjoy/"
DATA_ROOT = "/data/"
# font = DATA_ROOT+'fonts/SIMFANG.TTF'
# font = DATA_ROOT+'fonts/STXIHEI.TTF'
font='AR-PL-UKai-CN'
excel_content = pd.read_excel(DATA_ROOT+'text/text.xlsx')
title_list = excel_content["title"]
text_list = excel_content["text"]
end_list = excel_content["end"]
title = title_list[num]
text = text_list[num]
end = end_list[num]
print("标题：" + title)
print("内容：" + text)
print("结尾：" + end)

# 断句
sents = cut_sent(text)

# 调用tts生成语音：
# 命令格式：aspeak -t "你好，世界！" -l zh-CN -o ouput.wav -v zh-CN-XiaoqiuNeural -r -0.06
# for inx,val in enumerate(sents):
#     print(inx,val)
#     if inx >= 0:
#         subprocess.call(["aspeak -t "
#                          +val+
#                          " -l zh-CN -o "
#                          +DATA_ROOT+
#                          "dubbing/clip_out_"
#                          +str(inx)+
#                          ".wav -v zh-CN-XiaoqiuNeural -r -0.06"], shell=True)
#     time.sleep(5)

# "02 - Rainbow River.mp3"

# 生成一个背景图片
picture_file_name = ""
if args.picture is None: # 如果传的参数是None，就随机取一张图片
    picture_file_name = get_file_list(DATA_ROOT + "/picture")
elif args.picture == "1": # 如果传的参数是１，就用默认的图片
    picture_file_name = "blues-lee-zUsvn51N2Ro-unsplash.jpg"
else: # 如果有传数据，就用传的图片路径
    picture_file_name = args.picture
print("picture_file_name：" + picture_file_name)

# 调用背景图像生成一个基本的clip
my_clip = ImageClip(DATA_ROOT+"picture/"+picture_file_name)# has infinite duration
w,h = my_clip.size
my_clip = my_clip.fx(vfx.crop,x1=0, y1=0, x2=w, y2=w/1.88)
# my_clip = my_clip.fx(vfx.crop,x1=0, y1=0, x2=w, y2=w/2.35)
text_font_size = w*25/512
start_end_font_size = w*36/512

all_clip_list = [my_clip]
audio_clip_list = []
text_clip_start = 0
all_time = 0
title_time = 3
end_time = 5

# 设置开头标题
txt_clip = TextClip(title, fontsize=start_end_font_size, color='white', font=font)
txt_clip = txt_clip.set_pos('center').set_duration(title_time).set_start(text_clip_start)
all_clip_list.append(txt_clip)
text_clip_start = text_clip_start + title_time
all_time = all_time + title_time

# 视频叠加上文字和AI配音
for inx,val in enumerate(sents):
    audio_file_path = DATA_ROOT + "dubbing/clip_out_" + str(inx) + ".wav"
    duration = round(get_duration_wav(audio_file_path),2)
    print("text duration time = " + str(duration))

    # text_clip = TextClip("Hello", fontsize=70, stroke_width=5).resize(height=15)
    text_str = sents[inx]
    text_str = sub(text_str)
    txt_clip = TextClip(text_str,fontsize=text_font_size,color='white',font=font)

    # 增加遮罩
    # txt_w,txt_h = txt_clip.size
    # mask = color_split((2 * w // 3, h),
    #                    p1=(2, h), p2=(w // 3 + 2, 0),
    #                    col1=[255,0,0], col2=[0,255,0],
    #                    grad_width=2)
    # mask_clip = ImageClip(mask, ismask=True)
    # mask_clip = ImageClip(DATA_ROOT + "picture/meng.png", ismask=True)
    # txt_clip = txt_clip.set_pos('center').set_duration(duration).set_start(text_clip_start).set_mask(mask_clip)

    txt_clip = txt_clip.set_pos('center').set_duration(duration).set_start(text_clip_start)



    audioclip = AudioFileClip(audio_file_path).set_duration(duration).set_start(text_clip_start).volumex(2)
    text_clip_start = text_clip_start + duration

    all_clip_list.append(txt_clip)
    audio_clip_list.append(audioclip)
    all_time = all_time + duration

# 设置结尾
txt_clip = TextClip(end, fontsize=start_end_font_size, color='white', font=font)
txt_clip = txt_clip.set_pos('center').set_duration(end_time).set_start(text_clip_start)
all_clip_list.append(txt_clip)
text_clip_start = text_clip_start + end_time
all_time = all_time + end_time


video = CompositeVideoClip(all_clip_list)

# 生成一个背景音乐
music_file_name = ""
if args.music is None: # 如果传的参数是None，就随机取一首音乐
    music_file_name = get_file_list(DATA_ROOT + "/music")
elif args.music == "1": # 如果传的参数是１，就用默认的音乐
    music_file_name = "02 - Rainbow River.mp3"
else: # 如果有传数据，就用传的音乐路径
    music_file_name = args.music
print("music_file_name：" + music_file_name)

# 叠加上背景音乐
back_music_clip = AudioFileClip(DATA_ROOT+"music/" + music_file_name).subclip(t_start=0, t_end=all_time).volumex(0.5).audio_fadeout(end_time/2)
audio_clip_list.append(back_music_clip)
all_audio_clip = CompositeAudioClip(audio_clip_list)

video = video.set_audio(all_audio_clip)

print("all_time " +str(all_time))
print("video.size = " + str(video.size))

# 生成最终的视频
video.set_duration(all_time).set_fps(25).write_videofile(DATA_ROOT+"flower.avi",codec='mpeg4') # works

# 生成封面
video.save_frame(DATA_ROOT+"cover.png",t=1)
# my_clip.ipython_display()