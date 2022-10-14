import pandas as pd
import sys
import time
import argparse
import random
import numpy as np


from moviepy.editor import *
from clause import cut_sent,sub,cut_end,sentence_break
from file_operate import get_file_list,make_zip
from get_audio_time import get_duration_wav
from clip_tools import ai_dubbing,add_txt_mask,optimi_txt_clip,generate_cover
from moviepy.video.tools.drawing import color_gradient
from moviepy.video.tools.drawing import color_split

def generate_video(args):


    num = 0
    if args.num == 0: # 如果传的参数是0，就随机取一个整数
        num = random.randint(0,16)
    else: # 如果有传参数，就用传的参数
        num = args.num
    print("num：" + str(num))

    # 加载text数据
    DATA_ROOT = "/home/mocuili/data/enjoy/"
    # DATA_ROOT = "/data/enjoy/"
    font = DATA_ROOT+'fonts/SIMFANG.TTF'
    # font = DATA_ROOT+'fonts/STXIHEI.TTF'
    # font='AR-PL-UKai-CN'
    excel_content = pd.read_excel(DATA_ROOT+'text/text.xlsx')
    title_list = excel_content["title"]
    text_list = excel_content["text"]
    start_list = excel_content["start"]
    end_list = excel_content["end"]
    author_list = excel_content["author"]
    title = title_list[num] #标题是５－９个字长度最合适
    text = text_list[num]
    start = start_list[num]
    end = end_list[num]
    author = author_list[num]
    print("标题：" + str(title))
    print("开头：" + str(start))
    print("内容：" + str(text))
    print("结尾：" + str(end))
    print("作者：" + str(author))

    # 断句
    if args.template == 0:
        sents = cut_sent(text)
    else:
        sents = text.split('&')

    # 调用tts生成语音：
    ai_dubbing(args.dubbing,args.template,sents,DATA_ROOT)

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
    # my_clip = ImageClip(DATA_ROOT+"picture/"+picture_file_name)# has infinite duration
    my_clip = ImageClip(DATA_ROOT+"picture/picture3.jpg")
    w,h = my_clip.size
    my_clip = my_clip.fx(vfx.crop,x1=0, y1=0, x2=w, y2=w/1.88)
    # my_clip = my_clip.fx(vfx.crop,x1=0, y1=0, x2=w, y2=w/2.35)
    w,h = my_clip.size
    text_font_size = w/40
    start_end_font_size = w/20

    all_clip_list = [my_clip]
    audio_clip_list = []
    text_clip_start = 0
    all_time = 0
    title_time = 3
    end_time = 5

    # 设置开头标题
    txt_clip = TextClip(start, fontsize=start_end_font_size, color='white', font=font)
    txt_clip,colorclip = optimi_txt_clip(txt_clip,w,h,title_time,text_clip_start)
    all_clip_list.append(colorclip)
    all_clip_list.append(txt_clip)
    text_clip_start = text_clip_start + title_time
    all_time = all_time + title_time

    # 视频叠加上文字和AI配音
    for inx,val in enumerate(sents):

        text_str = sents[inx]
        if args.template == 0:
            audio_file_path = DATA_ROOT + "dubbing/clip_out_" + str(inx) + ".wav"
            duration = round(get_duration_wav(audio_file_path),2)
        else:
            duration = len(text_str)/7
        print("text duration time = " + str(duration))

        if args.template == 0:
            text_str = sub(text_str)
        else:
            text_str = "\""+sentence_break(text_str)+"\""
        txt_clip = TextClip(text_str,fontsize=text_font_size,color='white',font=font)

        txt_clip,colorclip = optimi_txt_clip(txt_clip,w,h,duration,text_clip_start)

        if args.template == 0:
            audioclip = AudioFileClip(audio_file_path).set_duration(duration).set_start(text_clip_start).volumex(2)
            audio_clip_list.append(audioclip)
        all_clip_list.append(colorclip)
        all_clip_list.append(txt_clip)
        text_clip_start = text_clip_start + duration
        all_time = all_time + duration

    # 设置结尾
    txt_clip = TextClip(cut_end(end), fontsize=start_end_font_size, color='white', font=font)
    txt_clip,colorclip = optimi_txt_clip(txt_clip,w,h,end_time,text_clip_start)
    all_clip_list.append(colorclip)
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
    back_music_clip = AudioFileClip(DATA_ROOT+"music/" + music_file_name).subclip(t_start=0, t_end=all_time).volumex(0.3).audio_fadeout(end_time/2)
    audio_clip_list.append(back_music_clip)
    all_audio_clip = CompositeAudioClip(audio_clip_list)

    video = video.set_audio(all_audio_clip)

    print("all_time " +str(all_time))
    print("video.size = " + str(video.size))


    # 生成横的封面
    # video.save_frame(DATA_ROOT+"cover.png",t=1)
    cover_clip = generate_cover(my_clip, DATA_ROOT, font, author, title)

    # 弄一个竖封面

    # 生成简介
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    RESULT_DIR = DATA_ROOT + "video/" + current_time + "/"

    # 保存最后的结果
    os.mkdir(RESULT_DIR);
    with open(RESULT_DIR + 'introduction.txt', 'w') as f:  # 设置文件对象
        f.write(title + "\n")
        f.write(text + "\n")
        f.write(end + "\n")
        f.write("BGM:"+ music_file_name.split('.')[0] + "\n")
    cover_clip.save_frame(RESULT_DIR + "cover.png", t=1)
    video.set_duration(all_time).set_fps(25).write_videofile(RESULT_DIR+"flower.mp4",codec='mpeg4') # works

    # 将结果放到zip压缩文件中
    make_zip(RESULT_DIR,DATA_ROOT + "video/"+ current_time + ".zip")


if __name__ == "__main__":

    # 接收参数
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--picture', type=str, default = None) #背景图片
    parser.add_argument('--music', type=str, default= None) #背景音乐
    parser.add_argument('--dubbing', type=int, default= 0) #AI配音
    parser.add_argument('--num', type=int, default= 0) #文字标号
    parser.add_argument('--template', type=int, default=0) #视频制作模板
    args = parser.parse_args()
    print("接受参数：picture：" + str(args.picture))
    print("接受参数：music：" + str(args.music))
    print("接受参数：dubbing：" + str(args.dubbing))
    print("接受参数：num：" + str(args.num))
    print("接受参数：template：" + str(args.template))

    generate_video(args)

