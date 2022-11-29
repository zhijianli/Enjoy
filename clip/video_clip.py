import pandas as pd
import sys
import psutil
import os
import gc
import time
import argparse
import random
import numpy as np
# import line_profiler
# profile = line_profiler.LineProfiler()
from memory_profiler import profile


from moviepy.editor import *
from clip.clause import *
from clip.file_operate import get_file_list,make_zip,copy_file,compress_image,copy_preview
from clip.get_audio_time import get_duration_wav
from clip.clip_tools import ai_dubbing,add_txt_mask,optimi_txt_clip,optimi_saying_clip,generate_cover
from tools.aliyun_oss import put_object_from_file
from moviepy.video.tools.drawing import color_gradient
from moviepy.video.tools.drawing import color_split
from guppy import hpy
from tools.my_logging import *

reading_speed = 2.5

# @profile
def generate_video(args):

    num = 0
    if args.num == 0: # 如果传的参数是0，就随机取一个整数
        num = random.randint(0,16)
    else: # 如果有传参数，就用传的参数
        num = args.num
    # info_log("num：" + str(num))

    # 加载text数据
    if args.env == "test":
        ROOT = "/home/mocuili/data/"
        DATA_ROOT = ROOT + "enjoy/"
    else:
        ROOT = "/data/"
        DATA_ROOT = ROOT + "enjoy/"

    # font = DATA_ROOT+'fonts/SIMFANG.TTF'
    font = DATA_ROOT + 'fonts/ZiXinFangMingKeBen(GuJiBan)-2.ttf'
    # comment_font = DATA_ROOT + 'fonts/ZiXinFangMingKeBen(GuJiBan)-2.ttf'
    comment_font = DATA_ROOT + 'fonts/SIMFANG.TTF'
    # font='AR-PL-UKai-CN'
    # font = DATA_ROOT + 'fonts/STXIHEI.TTF'
    excel_content = pd.read_excel(DATA_ROOT+'text/text.xlsx')
    title_list = excel_content["title"]
    text_list = excel_content["text"]
    start_list = excel_content["start"]
    end_list = excel_content["end"]
    author_list = excel_content["author"]
    provenance_list = excel_content["provenance"]
    title = title_list[num] #标题是５－９个字长度最合适
    text = text_list[num]
    start = start_list[num]
    end = end_list[num]
    author = author_list[num]
    provenance = provenance_list[num]
    # info_log("标题：" + str(title))
    # info_log("开头：" + str(start))
    # info_log("内容：" + str(text))
    # info_log("结尾：" + str(end))
    # info_log("作者：" + str(author))
    # info_log("出处：" + str(provenance))
    print("命令是： python3 video_clip.py --num="+str(num)+
          " --picture="+str(args.picture)+
          " --music="+str(args.music)+
          " --dubbing="+str(args.dubbing)+
          " --env="+str(args.env)+
          " --template="+str(args.template))

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
    info_log("背景图片名字：" + picture_file_name)

    # 调用背景图像生成一个基本的clip
    # my_clip = ImageSequenceClip(DATA_ROOT + "picture/" + picture_file_name,fps=5)
    my_clip = ImageClip(DATA_ROOT+"picture/"+picture_file_name)
    # my_clip = VideoFileClip(DATA_ROOT+"picture/"+picture_file_name)
    # my_clip = my_clip.loop(duration=my_clip.duration)

    w,h = my_clip.size
    my_clip = my_clip.fx(vfx.crop,x1=0, y1=0, x2=w, y2=w/1.88)
    # my_clip = my_clip.fx(vfx.crop,x1=0, y1=0, x2=w, y2=w/2.35)
    w,h = my_clip.size
    text_font_size = w*3/80
    start_end_font_size = w*2/40

    all_clip_list = [my_clip]
    audio_clip_list = []
    text_clip_start = 0
    all_time = 0
    title_time = 3
    end_time = 5
    dubbing_interval = 1 #多加1秒是因为要每一段语音之后间隔两秒

    # 设置开头标题
    # txt_clip = TextClip(start, fontsize=start_end_font_size, color='white', font=font)
    # txt_clip,colorclip = optimi_txt_clip(txt_clip,w,h,title_time,text_clip_start)
    # all_clip_list.append(colorclip)
    # all_clip_list.append(txt_clip)
    # text_clip_start = text_clip_start + title_time
    # all_time = all_time + title_time
    colorclip_ori_list = []

    # 视频叠加上文字和AI配音
    # info_log("sents"+sents)
    for inx,val in enumerate(sents):

        text_str = sents[inx]

        saying_comment = text_str.split('||')[0] #获取名言和评论

        source = text_str.split('||')[1] # 获取来源
        saying = saying_comment.split('++')[0]
        comment = saying_comment.split('++')[1]

        if args.dubbing > 0:
            audio_file_path = DATA_ROOT + "dubbing/clip_out_" + str(inx) + ".wav"
            duration = round(get_duration_wav(audio_file_path),2)+dubbing_interval
        else:
            duration = len(saying)//reading_speed
        # info_log("text duration time = " + str(duration))

        # if args.template == 0:
        #     saying = sub(saying)
        # else:
        #     # saying = "\"" + saying + "\""
        #     saying = sentence_break(saying)

        txt_clip = TextClip(saying,fontsize=text_font_size,color='white',font=font)
        comment_clip = TextClip(comment, fontsize=text_font_size // 1.5, color='white', font=comment_font)
        source_clip = TextClip(source, fontsize=text_font_size//1.5, color='white', font=comment_font)

        # 设置文字的剪辑信息
        txt_clip,colorclip,source_clip,comment_clip,colorclip_ori = optimi_saying_clip(txt_clip,w,h,duration,text_clip_start,source_clip,comment_clip,text_font_size)

        if args.dubbing > 0:
            audioclip = AudioFileClip(audio_file_path).set_duration(duration-dubbing_interval).set_start(text_clip_start).volumex(2)
            audio_clip_list.append(audioclip)
        # all_clip_list.append(colorclip)
        all_clip_list.append(txt_clip)
        all_clip_list.append(comment_clip)
        all_clip_list.append(source_clip)
        colorclip_ori_list.append(colorclip_ori)
        text_clip_start = text_clip_start + duration
        all_time = all_time + duration

    # 设置结尾
    txt_clip = TextClip(cut_end(end), fontsize=start_end_font_size, color='white', font=font)
    txt_clip,colorclip = optimi_txt_clip(txt_clip,w,h,end_time,text_clip_start)

    # all_clip_list.append(colorclip)
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
    info_log("背景音乐名字：" + music_file_name)

    # 叠加上背景音乐
    back_music_clip = AudioFileClip(DATA_ROOT+"music/" + music_file_name).subclip(t_start=0, t_end=all_time).volumex(0.3).audio_fadeout(end_time*0.7)
    audio_clip_list.append(back_music_clip)
    all_audio_clip = CompositeAudioClip(audio_clip_list)

    video = video.set_audio(all_audio_clip)

    info_log("视频总时长： " +str(all_time))
    info_log("视频尺寸：" + str(video.size))

    # 生成横的封面
    # video.save_frame(DATA_ROOT+"cover.png",t=1)
    cover_clip = generate_cover(my_clip, DATA_ROOT, font, author, title,args.font_cover_ratio)

    # 弄一个竖封面

    # 生成简介
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    RESULT_DIR = DATA_ROOT + "video/" + current_time + "/"

    # 生成标签
    # label_str = args.label
    # convert_label_str = ""
    # if label_str is not None and len(label_str) > 0:
    #     label_list = label_str.split('　')
    #     for label in label_list:
    #         convert_label_str = convert_label_str + "#"+str(label)+"　"

    # 保存最后的结果
    os.mkdir(RESULT_DIR);
    text = text.replace("++ ||", "－－");
    text = text.replace("&", "");
    text = text.replace("\n", "");
    text = text.replace("》", "》\n");
    text = labeled(text)

    with open(RESULT_DIR + 'introduction.txt', 'w') as f:  # 设置文件对象
        f.write(title + "\n")
        f.write(text + "\n")
        f.write(end + "\n")
        # f.write("出处:" + provenance + "\n")
        f.write("BGM:"+ music_file_name + "\n")
        f.write("图片名:" + picture_file_name + "\n")
        f.write("作者:" + author + "\n")
        # f.write("标签:" + str(convert_label_str) + "\n")

    cover_clip.save_frame(RESULT_DIR + "cover.png", t=1)

    # 保存压缩图
    # compress_image(RESULT_DIR + "cover.png")

    # 视频写入文件
    # video_name = "flower.webm"
    # video.set_duration(all_time).set_fps(5).write_videofile(RESULT_DIR+video_name,codec='libvpx')
    video_name = "flower.mp4"
    video.set_duration(all_time).set_fps(15).write_videofile(RESULT_DIR + video_name, codec='libx264')

    # 每次编辑完视频之后都要主动释放内存，进行垃圾回收
    del cover_clip
    del video
    all_clip_len = len(all_clip_list)
    colorclip_ori_len = len(colorclip_ori_list)
    for index in range(all_clip_len):
        del all_clip_list[all_clip_len-1-index]
    for index in range(colorclip_ori_len):
        del colorclip_ori_list[colorclip_ori_len-1-index]

    gc.collect()

    # 将结果放到zip压缩文件中
    # make_zip(RESULT_DIR,DATA_ROOT + "video/"+ current_time + ".zip")

    info_log("=============视频生成结束！=============")

    # # 拷贝文件
    # if args.env == "prod":
    #     DATA_OSS_ROOT = ROOT+"enjoy-oss/"
    #     copy_file(DATA_ROOT + "video/"+ current_time, DATA_OSS_ROOT + "video/"+ current_time)
    #     print("=============视频拷贝结束！=============")

    # 文件上传到oss
    cover_url = put_object_from_file("video/" + current_time + "/cover.png",
                                     DATA_ROOT + "video/" + current_time + "/cover.png")
    video_url = put_object_from_file("video/" + current_time + "/" + video_name,
                                     DATA_ROOT + "video/" + current_time + "/" + video_name)
    put_object_from_file("video/" + current_time + "/introduction.txt",
                                          DATA_ROOT + "video/" + current_time + "/introduction.txt")

    info_log("=============视频上传结束！=============")

    m, s = divmod(all_time, 60)
    video_time = str(int(m)) + "分" + str(int(s)) + "秒"

    # 多睡眠两秒，好让前端日志显示完整
    time.sleep(2)

    return cover_url,video_url,title,music_file_name,picture_file_name,author,video_time


def preview(args):
    num = 0
    if args.num == 0:  # 如果传的参数是0，就随机取一个整数
        num = random.randint(0, 16)
    else:  # 如果有传参数，就用传的参数
        num = args.num
    # info_log("num：" + str(num))

    # 加载text数据
    if args.env == "test":
        ROOT = "/home/mocuili/data/"
        DATA_ROOT = ROOT + "enjoy/"
    else:
        ROOT = "/data/"
        DATA_ROOT = ROOT + "enjoy/"

    font = DATA_ROOT + 'fonts/ZiXinFangMingKeBen(GuJiBan)-2.ttf'
    # comment_font = DATA_ROOT + 'fonts/ZiXinFangMingKeBen(GuJiBan)-2.ttf'
    comment_font = DATA_ROOT + 'fonts/SIMFANG.TTF'
    excel_content = pd.read_excel(DATA_ROOT + 'text/text.xlsx')
    title_list = excel_content["title"]
    text_list = excel_content["text"]
    start_list = excel_content["start"]
    end_list = excel_content["end"]
    author_list = excel_content["author"]
    provenance_list = excel_content["provenance"]
    title = title_list[num]  # 标题是５－９个字长度最合适
    text = text_list[num]
    start = start_list[num]
    end = end_list[num]
    author = author_list[num]
    provenance = provenance_list[num]
    # info_log("标题：" + str(title))
    # info_log("开头：" + str(start))
    # info_log("内容：" + str(text))
    # info_log("结尾：" + str(end))
    # info_log("作者：" + str(author))
    # info_log("出处：" + str(provenance))
    print("命令是： python3 video_clip.py --num=" + str(num) +
          " --picture=" + str(args.picture) +
          " --music=" + str(args.music) +
          " --dubbing=" + str(args.dubbing) +
          " --env=" + str(args.env) +
          " --template=" + str(args.template))

    # 断句
    if args.template == 0:
        sents = cut_sent(text)
    else:
        sents = text.split('&')

    # 调用tts生成语音：
    ai_dubbing(args.dubbing, args.template, sents, DATA_ROOT)

    # 生成一个背景图片
    picture_file_name = ""
    if args.picture is None:  # 如果传的参数是None，就随机取一张图片
        picture_file_name = get_file_list(DATA_ROOT + "/picture")
    elif args.picture == "1":  # 如果传的参数是１，就用默认的图片
        picture_file_name = "blues-lee-zUsvn51N2Ro-unsplash.jpg"
    else:  # 如果有传数据，就用传的图片路径
        picture_file_name = args.picture

    # 调用背景图像生成一个基本的clip
    my_clip = ImageClip(DATA_ROOT + "picture/" + picture_file_name)

    w, h = my_clip.size
    my_clip = my_clip.fx(vfx.crop, x1=0, y1=0, x2=w, y2=w / 1.88)
    w, h = my_clip.size
    text_font_size = w*3/80
    start_end_font_size = w*3/40
    text_clip_start = 0
    title_time = 3
    end_time = 5
    preview_size = 1000
    all_time = 0
    title_time = 3
    end_time = 5
    duration = 0
    dubbing_interval = 1  # 多加1秒是因为要每一段语音之后间隔两秒

    # 创建预览结果的文件夹
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    PREVIEW_DIR = DATA_ROOT + "preview/" + current_time + "/"
    os.mkdir(PREVIEW_DIR);

    # 生成开头标题的图片帧
    # start_clip_list = [my_clip]
    # txt_clip = TextClip(start, fontsize=start_end_font_size, color='white', font=font)
    # txt_clip, colorclip = optimi_txt_clip(txt_clip, w, h, title_time, text_clip_start)
    # # start_clip_list.append(colorclip)
    # start_clip_list.append(txt_clip)
    # start_clip = CompositeVideoClip(start_clip_list)
    # start_clip.resize(width=preview_size).save_frame(PREVIEW_DIR + "start_clip.png", t=1)
    # all_time = all_time + title_time

    saying_clip_frame_list = []

    # 视频叠加上文字，生成中间的文字帧
    for inx, val in enumerate(sents):

        text_str = sents[inx]
        saying_comment = text_str.split('||')[0]  # 获取名言和评论
        source = text_str.split('||')[1]  # 获取来源
        saying = saying_comment.split('++')[0]
        comment = saying_comment.split('++')[1]

        if args.dubbing > 0:
            audio_file_path = DATA_ROOT + "dubbing/clip_out_" + str(inx) + ".wav"
            duration = round(get_duration_wav(audio_file_path), 2) + dubbing_interval
        else:
            duration = len(saying) // reading_speed
        info_log("句子时长 = " + str(duration))
        all_time = all_time + duration

        saying_clip_list = [my_clip]

        # if args.template == 0:
        #     saying = sub(saying)
        # else:
        #     saying = sentence_break(saying)
        txt_clip = TextClip(saying, fontsize=text_font_size, color='white', font=font)
        comment_clip = TextClip(comment, fontsize=text_font_size // 1.5, color='white', font=comment_font)
        source_clip = TextClip(source, fontsize=text_font_size // 1.5, color='white', font=comment_font)

        # 设置文字的剪辑信息
        txt_clip, colorclip, source_clip, comment_clip, colorclip_ori = optimi_saying_clip(txt_clip, w, h, 2,
                                                                                           text_clip_start, source_clip,
                                                                                           comment_clip,text_font_size)

        # saying_clip_list.append(colorclip)
        saying_clip_list.append(txt_clip)
        saying_clip_list.append(comment_clip)
        saying_clip_list.append(source_clip)
        saying_clip = CompositeVideoClip(saying_clip_list)
        saying_clip.resize(width=preview_size).save_frame(PREVIEW_DIR + "saying_clip_"+str(inx)+".png", t=1)
        saying_clip_frame_list.append("saying_clip_"+str(inx)+".png")

        del colorclip_ori
        del colorclip
        del txt_clip
        del comment_clip
        del source_clip
        del saying_clip
        gc.collect()

    # 生成结尾帧
    end_clip_list = [my_clip]
    txt_clip = TextClip(cut_end(end), fontsize=start_end_font_size, color='white', font=font)
    txt_clip, colorclip = optimi_txt_clip(txt_clip, w, h, end_time, text_clip_start)

    # end_clip_list.append(colorclip)
    end_clip_list.append(txt_clip)
    end_clip = CompositeVideoClip(end_clip_list)
    end_clip.resize(width=preview_size).save_frame(PREVIEW_DIR + "end_clip.png", t=1)
    all_time = all_time + end_time

    # 生成横的封面帧
    cover_clip = generate_cover(my_clip, DATA_ROOT, font, author, title,args.font_cover_ratio)
    cover_clip.resize(width=preview_size).save_frame(PREVIEW_DIR + "cover.png", t=1)

    # 生成一个背景音乐
    music_file_name = ""
    if args.music is None: # 如果传的参数是None，就随机取一首音乐
        music_file_name = get_file_list(DATA_ROOT + "/music")
    elif args.music == "1": # 如果传的参数是１，就用默认的音乐
        music_file_name = "02 - Rainbow River.mp3"
    else: # 如果有传数据，就用传的音乐路径
        music_file_name = args.music

    # 生成标签
    # label_str = args.label
    # convert_label_str = ""
    # if label_str is not None and len(label_str) > 0:
    #     label_list = label_str.split('　')
    #     for label in label_list:
    #         convert_label_str = convert_label_str + "#"+str(label)+"　"

    # 生成简介
    with open(PREVIEW_DIR + 'introduction.txt', 'w') as f:  # 设置文件对象
        f.write(title + "\n")
        f.write(text + "\n")
        f.write(end + "\n")
        # f.write("出处:" + provenance + "\n")
        f.write("BGM:" + music_file_name + "\n")
        f.write("图片名:" + picture_file_name + "\n")
        f.write("作者:" + author + "\n")
        # f.write("标签:" + str(convert_label_str) + "\n")

    # 删除内存
    del my_clip
    del cover_clip
    # del start_clip
    del end_clip

    gc.collect()

    # 上次文件到阿里云oss
    info_log("=============预览拷贝开始！============="+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    frame_list = []
    cover_url = put_object_from_file("preview/" + current_time + "/cover.png",
                                   DATA_ROOT + "preview/" + current_time + "/cover.png")
    frame_list.append(cover_url)

    # start_clip_url = put_object_from_file("preview/" + current_time + "/start_clip.png",
    #                                DATA_ROOT + "preview/" + current_time + "/start_clip.png")
    # frame_list.append(start_clip_url)

    for saving_clip_frame in saying_clip_frame_list:
        saving_clip_url = put_object_from_file("preview/" + current_time + "/"+saving_clip_frame,
                                              DATA_ROOT + "preview/" + current_time + "/"+saving_clip_frame)
        frame_list.append(saving_clip_url)

    end_clip_url = put_object_from_file("preview/" + current_time + "/end_clip.png",
                                          DATA_ROOT + "preview/" + current_time + "/end_clip.png")

    put_object_from_file("preview/" + current_time + "/introduction.txt",
                                          DATA_ROOT + "preview/" + current_time + "/introduction.txt")

    info_log("=============预览拷贝结束！============="+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    m, s = divmod(all_time, 60)
    video_time = str(int(m)) + "分" + str(int(s)) + "秒"
    info_log("视频总时长:"+video_time)
    frame_list.append(end_clip_url)

    # 多睡眠两秒，好让前端日志显示完整
    time.sleep(2)

    return frame_list,title,music_file_name,picture_file_name,author,video_time




if __name__ == "__main__":

    # 接收参数
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--picture', type=str, default = None) #背景图片
    parser.add_argument('--music', type=str, default= None) #背景音乐
    parser.add_argument('--dubbing', type=int, default= 0) #AI配音
    parser.add_argument('--num', type=int, default= 0) #文字标号
    parser.add_argument('--template', type=int, default=0) #视频制作模板
    parser.add_argument('--uploadoss', type=int, default=0)  # 是否上传oss
    parser.add_argument('--env', type=str, default= "test") #环境
    args = parser.parse_args()
    print("接受参数：picture：" + str(args.picture))
    print("接受参数：music：" + str(args.music))
    print("接受参数：dubbing：" + str(args.dubbing))
    print("接受参数：num：" + str(args.num))
    print("接受参数：template：" + str(args.template))
    print("接受参数：uploadoss：" + str(args.uploadoss))
    print("接受参数：env：" + str(args.env))

    generate_video(args)

