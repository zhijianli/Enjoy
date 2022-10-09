
from moviepy.editor import *
import time
import subprocess

# 命令格式：aspeak -t "你好，世界！" -l zh-CN -o ouput.wav -v zh-CN-XiaoqiuNeural -r -0.06
def ai_dubbing(is_dubbing,sents,DATA_ROOT):
    print("开始AI配音")
    if is_dubbing > 0:
        for inx,val in enumerate(sents):
            print(inx,val)
            if inx >= 0:
                while True:
                    dubbing_result = subprocess.call(["aspeak -t "
                                     +val+
                                     " -l zh-CN -o "
                                     +DATA_ROOT+
                                     "dubbing/clip_out_"
                                     +str(inx)+
                                     ".wav -v zh-CN-XiaoqiuNeural -r -0.06"], shell=True)
                    print("dubbing_result: " + str(dubbing_result))
                    if str(dubbing_result) == "0":
                        break
                    else:
                        time.sleep(10)

            time.sleep(5)


def add_mask(txt_clip,duration,text_clip_start):
    txt_w, txt_h = txt_clip.size
    colorclip = ColorClip(size=(txt_w * 6 // 5, txt_h * 6 // 5), color=[00, 00, 00]).set_opacity(
        0.3).set_pos('center').set_duration(duration).set_start(text_clip_start)
    return colorclip

if __name__ == "__main__":

    DATA_ROOT = "/home/mocuili/data/enjoy/"
    # font = 'AR-PL-UKai-CN'
    # title = "如何探寻爱的真谛？"
    # cover_clip_list = []
    # cover_pitcure_clip = ImageClip(DATA_ROOT + "picture/nasa-HWIOLU7_O6w-unsplash.jpg")
    # cover_w,cover_h = cover_pitcure_clip.size
    # cover_pitcure_clip = cover_pitcure_clip.fx(vfx.crop, x1=0, y1=0, x2=cover_w, y2=cover_w / 1.88)
    #
    #
    # txt_clip = TextClip(title, fontsize=cover_w*50/512, color='white', font=font)
    # txt_clip = txt_clip.set_pos('center').set_duration(1).set_start(1)
    # txt_w,txt_h = txt_clip.size
    #
    # colorclip = ColorClip(size=(txt_w * 6 // 5,txt_h*6//5), color=[00,00,00],duration=10).set_opacity(0.3).set_pos('center')
    #
    # cover_clip_list.append(cover_pitcure_clip)
    # cover_clip_list.append(colorclip)
    # cover_clip_list.append(txt_clip)
    # cover_clip = CompositeVideoClip(cover_clip_list)
    #
    #
    # cover_clip.save_frame(DATA_ROOT + "cover.png", t=1)
    # sents = ["你好啊你好啊你好啊你好啊你好啊你好啊你好啊","你好啊你好啊你好啊你好啊你好啊你好啊你好啊",
    #          "你好啊你好啊你好啊你好啊你好啊你好啊你好啊","你好啊你好啊你好啊你好啊你好啊你好啊你好啊",
    #          "你好啊你好啊你好啊你好啊你好啊你好啊你好啊","你好啊你好啊你好啊你好啊你好啊你好啊你好啊"]
    # ai_dubbing(1,sents,DATA_ROOT)

