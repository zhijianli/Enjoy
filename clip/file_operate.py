import random
import os, zipfile
import shutil
from PIL import Image
import librosa
import soundfile as sf
from urllib.request import urlretrieve

def get_file_list(dir):
    file_list = []
    for root, dirs, files in os.walk(dir, topdown=False):
        file_list = files
    file_name = random.choice(file_list)
    print(file_name)
    return file_name

def get_file_name_list(dir):
    file_list = []
    for root, dirs, files in os.walk(dir, topdown=False):
        file_list = files
    return file_list

#打包目录为zip文件（未压缩）
def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)     #相对路径
            zipf.write(pathfile, arcname)
    zipf.close()

def copy_file(source_file,destination_file):
    shutil.copyfile(source_file+".zip",destination_file+".zip")
    shutil.copytree(source_file, destination_file)

def copy_preview(source_file,destination_file):
    shutil.copytree(source_file, destination_file)

def get_outfile(infile, outfile):
    if outfile:
        return outfile
    dir, suffix = os.path.splitext(infile)
    outfile = '{}-out{}'.format(dir, suffix)
    return outfile

def compress_image(infile,scaleDown,outfile=''):

    outfile = get_outfile(infile, outfile)
    img = Image.open(infile)
    w, h = img.size
    w, h = round(w * scaleDown), round(h * scaleDown)
    img = img.resize((w, h), Image.ANTIALIAS)
    img.save(outfile, optimize=True, quality=85)

def urllib_download(image_url,local_path):
    urlretrieve(image_url, local_path)

if __name__ == "__main__":
    title = "你好"
    DATA_ROOT = "/home/mocuili/data/enjoy/"
    # urllib_download("http://viapi-cn-shanghai-dha-segmenter.oss-cn-shanghai.aliyuncs.com/upload/result_humansegmenter/2022-11-10/invi_humansegmenter_016680706097581328967_YT1oTe.png?Expires=1668072409&OSSAccessKeyId=LTAI4FoLmvQ9urWXgSRpDvh1&Signature=rHErvgq4N0fgrONKF%2FUNq3yNdCM%3D",DATA_ROOT+"avatar/111.png")
    # file_name = get_file_list(DATA_ROOT+"/music")
    # make_zip("/home/mocuili/data/enjoy/video/121/","/home/mocuili/data/enjoy/video/121.zip")
    # copy_file(DATA_ROOT + "video/2022-10-14 15:19:44", "/home/mocuili/data/enjoy-oss/video/2022-10-14 15:19:44.zip")
    compress_image(DATA_ROOT+"cover.jpg",0.3)
    # music_name = "whatsup"
    # file_name = music_name+".mp3"
    # new_file_name = music_name+"-16k.mp3"
    # y,sr = librosa.load(DATA_ROOT+file_name,sr=44100)
    # y_16k = librosa.resample(y,sr,16000)
    # librosa.output.write_wav(DATA_ROOT+new_file_name,y_16k,16000)

    # data,samplerate = sf.read(DATA_ROOT+file_name)
    # sf.write(DATA_ROOT+new_file_name,data,16000)


