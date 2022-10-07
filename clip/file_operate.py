import os
import random

def get_file_list(dir):
    file_list = []
    for root, dirs, files in os.walk(dir, topdown=False):
        file_list = files
    file_name = random.choice(file_list)
    print(file_name)
    return file_name


if __name__ == "__main__":

    DATA_ROOT = "/home/mocuili/data/enjoy/"
    file_name = get_file_list(DATA_ROOT+"/music")
