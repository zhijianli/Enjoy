import logging as lg
import os,time

class logging_():
    def __init__(self,path,name, delete=True):
        self.path = path  # 日志文件存放位置
        self.log_ = os.path.join(self.path, name)  # 进入文件目录
        if delete == True:
            open(f"{path}/{name}", "w").close  # 为True时清空文本

        # 创建一个日志处理器
        self.logger = lg.getLogger('logger')
        # 设置日志等级，低于设置等级的日志被丢弃
        self.logger.setLevel(lg.DEBUG)
        # 设置输出日志格式
        self.fmt = lg.Formatter("[%(asctime)s] - %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")
        # 创建一个文件处理器
        self.fh = lg.FileHandler(self.log_, encoding='utf-8')
        # 设置文件输出格式
        self.fh.setFormatter(self.fmt)
        # 将文件处理器添加到日志处理器中
        self.logger.addHandler(self.fh)
        # 创建一个控制台处理器
        self.sh = lg.StreamHandler()
        # 设置控制台输出格式
        self.sh.setFormatter(self.fmt)
        # 将控制台处理器添加到日志处理器中
        self.logger.addHandler(self.sh)

        # 关闭文件
        self.fh.close()


# 创建方法生成日志
def generation_log():
    for i in range(200):
        lg.info(i)
        # time.sleep(1)


# 读取日志并返回
def red_logs(_path,log_name):
    log_path = f'{_path}{log_name}'  # 获取日志文件路径
    with open(log_path, 'rb') as f:
        log_size = os.path.getsize(log_path)  # 获取日志大小
        offset = -100
        # 如果文件大小为0时返回空
        if log_size == 0:
            return ''
        while True:
            # 判断offset是否大于文件字节数,是则读取所有行,并返回
            if (abs(offset) >= log_size):
                f.seek(-log_size, 2)
                data = f.readlines()
                return data
            # 游标移动倒数的字节数位置
            data = f.readlines()
            # 判断读取到的行数，如果大于1则返回最后一行，否则扩大offset
            if (len(data) > 1):
                return data
            else:
                offset *= 2


# 使用
if __name__ == '__main__':
    env = os.environ["DEVELOP_ENV"]
    if env == "test":
        _path = "/home/mocuili/data/"
    if env == "prod":
        _path = "/data/"
    log_name = "video_clip.log"
    lg = logging_(_path,log_name).logger  # 实例化封装类

    # lg.info('1111')
    # lg.debug('2222')
    # lg.error('33333')
    # lg.warning('44444')
    generation_log()

    data = red_logs(_path,log_name)

    print(data)
