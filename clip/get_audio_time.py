
import wave
import contextlib


def get_duration_wav(file_path):
    """
    获取wav音频文件时长
    :param file_path:
    :return:
    """
    with contextlib.closing(wave.open(file_path, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    return duration




if __name__ == "__main__":
    file_path = '/home/mocuili/data/enjoy/dubbing/clip_out_1.wav'

    duration = get_duration_wav(file_path)

    print(duration)


