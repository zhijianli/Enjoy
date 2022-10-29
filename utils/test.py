from moviepy.editor import VideoFileClip
from guppy import hpy
import sys
from memory_profiler import profile

DATA_ROOT = "/home/mocuili/data/enjoy/"

@profile
def main():
    clip = VideoFileClip(DATA_ROOT+'9957.gif_wh860.gif')
    if len(sys.argv) > 1 and sys.argv[1] == 'del':
        del clip.make_frame

h = hpy()
h.setrelheap()
main()
print(h.heap())