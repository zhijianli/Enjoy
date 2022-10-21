import random
import os, zipfile
import shutil
from PIL import Image

def get_file_list(dir):
    file_list = []
    for root, dirs, files in os.walk(dir, topdown=False):
        file_list = files
    file_name = random.choice(file_list)
    print(file_name)
    return file_name


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

def get_outfile(infile, outfile):
    if outfile:
        return outfile
    dir, suffix = os.path.splitext(infile)
    outfile = '{}-out{}'.format(dir, suffix)
    return outfile

def compress_image(infile, outfile=''):

    outfile = get_outfile(infile, outfile)
    img = Image.open(infile)
    w, h = img.size
    w, h = round(w * 0.2), round(h * 0.2)
    img = img.resize((w, h), Image.ANTIALIAS)
    img.save(outfile, optimize=True, quality=85)


if __name__ == "__main__":
    title = "你好"
    DATA_ROOT = "/home/mocuili/data/enjoy/"
    # file_name = get_file_list(DATA_ROOT+"/music")
    # make_zip("/home/mocuili/data/enjoy/video/121/","/home/mocuili/data/enjoy/video/121.zip")
    # copy_file(DATA_ROOT + "video/2022-10-14 15:19:44", "/home/mocuili/data/enjoy-oss/video/2022-10-14 15:19:44.zip")
    compress_image(DATA_ROOT+"cover.png")

