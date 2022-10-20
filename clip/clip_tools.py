
from moviepy.editor import *
import time
import subprocess

# 命令格式：aspeak -t "你好，世界！" -l zh-CN -o ouput.wav -v zh-CN-XiaoqiuNeural -r -0.06
def ai_dubbing(is_dubbing,template,sents,DATA_ROOT):
    print("开始AI配音")
    if is_dubbing > 0:
        for inx,val in enumerate(sents):
            print(inx,val)
            if inx >= 0:
                while True:
                    dubbing_order = f"aspeak -t '{val}' -l zh-CN -o {DATA_ROOT}dubbing/clip_out_{inx}.wav -v zh-CN-XiaoqiuNeural -r -0.06"
                    print("dubbing_order：" + dubbing_order)
                    dubbing_result = subprocess.call([dubbing_order], shell=True)
                    print("dubbing_result: " + str(dubbing_result))
                    if str(dubbing_result) == "0":
                        break
                    else:
                        time.sleep(10)

            time.sleep(5)

def optimi_txt_clip(txt_clip,w,h,duration,text_clip_start):
    txt_w, txt_h = txt_clip.size
    position = ((w - txt_w) // 2, (h - txt_h)//2 * 9//10)
    txt_clip = txt_clip.set_position(position).set_duration(duration).set_start(text_clip_start)

    # 增加遮罩
    colorclip = add_txt_mask(txt_clip,duration,text_clip_start,w,h)

    return txt_clip,colorclip

def optimi_txt_source_clip(txt_clip,w,h,duration,text_clip_start,source_clip):
    txt_w, txt_h = txt_clip.size
    position = ((w - txt_w) // 2, (h - txt_h)//2 * 9//10)
    txt_clip = txt_clip.set_position(position).set_duration(duration).set_start(text_clip_start)

    # 增加遮罩
    colorclip = add_txt_mask(txt_clip,duration,text_clip_start,w,h)

    # 设置来源的剪辑信息
    source_w,source_h = source_clip.size
    color_w,color_h = colorclip.size
    # 来源的位置：x位置是遮罩的x位置+遮罩的w-来源的w,y位置是遮罩的y+遮罩的h*11/10
    source_x = (w - txt_w)//2-txt_w//10 + color_w - source_w
    source_y = ((h - txt_h)//2 - h*3//40) * 9//10 + color_h*6//5
    source_clip = source_clip.set_position((source_x,source_y)).set_duration(duration).set_start(text_clip_start)

    return txt_clip,colorclip,source_clip

def add_txt_mask(txt_clip,duration,text_clip_start,w,h):
    txt_w, txt_h = txt_clip.size
    colorclip = ColorClip(size=(txt_w*6//5, txt_h+h*3//20), color=[00, 00, 00]).set_opacity(
        0.3).set_position(((w - txt_w)//2 - txt_w//10, ((h - txt_h)//2 - h*3//40) * 9//10)).set_duration(duration).set_start(text_clip_start)
    return colorclip

def generate_cover(cover_pitcure_clip,DATA_ROOT,font,author_name,title):
    # 封面图
    cover_clip_list = []
    cover_w, cover_h = cover_pitcure_clip.size
    cover_pitcure_clip = cover_pitcure_clip.fx(vfx.crop, x1=0, y1=0, x2=cover_w, y2=cover_w / 1.88)
    cover_w, cover_h = cover_pitcure_clip.size
    print("生成封面图")

    # 标题
    txt_clip = TextClip(title, fontsize=cover_w / 20, color='white', font=font)
    txt_clip = txt_clip.set_duration(1).set_start(1)
    txt_w, txt_h = txt_clip.size
    print("生成封面标题")

    # 作者
    author_clip = TextClip(author_name, fontsize=cover_w / 30, color='white', font=font)
    author_clip = author_clip.set_duration(1).set_start(1)
    print("生成封面作者")

    # 头像
    avatar_clip = ImageClip(DATA_ROOT + "avatar/"+author_name+".jpg")
    avatar_w,avatar_h = avatar_clip.size
    avatar_resize = (cover_h/avatar_h)/2
    avatar_w = avatar_w * avatar_resize
    avatar_h = avatar_h * avatar_resize
    avatar_x = (cover_w - txt_w - avatar_w) // 2-cover_w//42
    avatar_y = (cover_h-avatar_h)//2*9//10
    avatar_clip = avatar_clip.resize(avatar_resize)
    print("生成封面头像")

    # 遮罩
    colorclip_w = int(cover_w*8//10)
    colorclip_h = int(avatar_h * 9 // 10)
    colorclip = ColorClip(size=(colorclip_w, colorclip_h), color=[00, 00, 00], duration=10).set_opacity(
        0.3)
    print("生成封面遮罩")


    # 线框
    line_width = colorclip_h//253
    wireframe_top_clip = ColorClip((cover_w*8//10, line_width), (255, 255, 255))
    wireframe_bottom_clip = ColorClip((cover_w*8//10, line_width), (255, 255, 255))
    wireframe_left_clip = ColorClip((line_width, colorclip_h), (255, 255, 255))
    wireframe_right_clip = ColorClip((line_width, colorclip_h + line_width), (255, 255, 255))
    print("生成封面线框")

    # 设置位置
    position = (avatar_x, avatar_y)
    txt_clip = txt_clip.set_position(((cover_w-avatar_w-txt_w)//2+avatar_w,cover_h//2))
    author_clip = author_clip.set_position(((cover_w-avatar_w-txt_w)//2+avatar_w,cover_h//2-txt_h))
    avatar_clip = avatar_clip.set_position(position)
    colorclip = colorclip.set_position((cover_w//10,avatar_y+avatar_h*1//10))
    wireframe_top_clip_x = cover_w*11//100
    wireframe_top_clip_y = avatar_y + avatar_h * 1 // 10 + colorclip_h // 20
    # print("白框x轴",(wireframe_top_clip_x,wireframe_top_clip_y))
    # print("头像位置", position)
    # print("遮罩位置", (cover_w//10,avatar_y+avatar_h*1//10))
    wireframe_top_clip = wireframe_top_clip.set_position((wireframe_top_clip_x, wireframe_top_clip_y))
    wireframe_bottom_clip = wireframe_bottom_clip.set_position((wireframe_top_clip_x, wireframe_top_clip_y + colorclip_h))
    wireframe_left_clip = wireframe_left_clip.set_position((wireframe_top_clip_x, wireframe_top_clip_y))
    wireframe_right_clip = wireframe_right_clip.set_position((wireframe_top_clip_x+colorclip_w, wireframe_top_clip_y))
    print("调整封面位置")

    cover_clip_list.append(cover_pitcure_clip)
    cover_clip_list.append(wireframe_top_clip)
    cover_clip_list.append(wireframe_bottom_clip)
    cover_clip_list.append(wireframe_left_clip)
    cover_clip_list.append(wireframe_right_clip)
    cover_clip_list.append(colorclip)
    cover_clip_list.append(avatar_clip)
    cover_clip_list.append(txt_clip)
    cover_clip_list.append(author_clip)
    cover_clip = CompositeVideoClip(cover_clip_list)
    print("封面剪辑叠加")

    return cover_clip


if __name__ == "__main__":

    DATA_ROOT = "/home/mocuili/data/enjoy/"
    font = DATA_ROOT+'fonts/SIMFANG.TTF'
    # author_name = "弗洛姆"
    author_name = "赫尔曼.黑塞"
    # author_name = "弗洛伊德"
    title = "如何探寻爱的真谛？"
    # cover_clip_list = []
    # cover_pitcure_clip = ImageClip(DATA_ROOT + "picture/nasa-HWIOLU7_O6w-unsplash.jpg")
    # cover_w,cover_h = cover_pitcure_clip.size
    # cover_pitcure_clip = cover_pitcure_clip.fx(vfx.crop, x1=0, y1=0, x2=cover_w, y2=cover_w / 1.88)
    # cover_w, cover_h = cover_pitcure_clip.size
    #
    # txt_clip = TextClip(title, fontsize=cover_w/20, color='white', font=font)
    # txt_clip,colorclip = optimi_txt_clip(txt_clip, cover_w, cover_h, 1, 1)
    #
    #
    #
    # cover_clip_list.append(cover_pitcure_clip)
    # cover_clip_list.append(colorclip)
    #
    # cover_clip_list.append(txt_clip)
    # cover_clip = CompositeVideoClip(cover_clip_list)
    cover_pitcure_clip = ImageClip(DATA_ROOT + "picture/shunsuke-ono-aisdACssFv4-unsplash.jpg")
    # cover_pitcure_clip = ImageClip(DATA_ROOT + "picture/nasa-HWIOLU7_O6w-unsplash.jpg")
    # cover_pitcure_clip = ImageClip(DATA_ROOT + "picture/xing.jpg")
    cover_clip = generate_cover(cover_pitcure_clip,DATA_ROOT,font,author_name,title)
    cover_clip.save_frame(DATA_ROOT + "cover.png", t=1)


