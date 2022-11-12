import oss2, uuid
import time
from itertools import islice

access_key_id = "LTAI5tSb4MDsMSxgQSzAYEDt"
access_key_secret = "LegWcAIgnqSIndlJUlYDnbhm9xKiVM"
auth = oss2.Auth(access_key_id, access_key_secret)
bucket_name = "enjoy-mocuili"
endpoint = "oss-cn-hangzhou.aliyuncs.com"
bucket = oss2.Bucket(auth, endpoint, bucket_name)


def put_object_from_file(name, file):
    bucket.put_object_from_file(name, file)
    return "https://{}.{}/{}".format(bucket_name, endpoint, name)




def get_bucket_list(suffix):
    obj_list = []
    # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
    auth = oss2.Auth(access_key_id, access_key_secret)
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth, 'http://'+endpoint, bucket_name)

    # oss2.ObjectIterator用于遍历文件。
    for obj in oss2.ObjectIterator(bucket, prefix='picture/'):
        if(obj.key.endswith(suffix)):
            split_list = obj.key.split("/", 1)
            obj_list.append(split_list[1])

    return obj_list


if __name__ == "__main__":
    # aliyunoss = AliyunOss()
    # DATA_ROOT = "/home/mocuili/data/enjoy/"
    # current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # img_url = put_object_from_file("preview/"+current_time+"/cover.jpg", DATA_ROOT+"cover.jpg")
    # print(img_url)
    get_bucket_list(".jpg")

