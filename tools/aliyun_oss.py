import oss2, uuid
import time

access_key_id = "LTAI5tSb4MDsMSxgQSzAYEDt"
access_key_secret = "LegWcAIgnqSIndlJUlYDnbhm9xKiVM"
auth = oss2.Auth(access_key_id, access_key_secret)
bucket_name = "enjoy-mocuili"
endpoint = "oss-cn-hangzhou.aliyuncs.com"
bucket = oss2.Bucket(auth, endpoint, bucket_name)


def put_object_from_file(name, file):
    bucket.put_object_from_file(name, file)
    return "https://{}.{}/{}".format(bucket_name, endpoint, name)



if __name__ == "__main__":
    # aliyunoss = AliyunOss()
    DATA_ROOT = "/home/mocuili/data/enjoy/"
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    img_url = put_object_from_file("preview/"+current_time+"/cover.jpg", DATA_ROOT+"cover.jpg")
    print(img_url)
