import requests
import json
from urllib import parse
from tools.aliyun_oss import *
from tools.mysql_tools import *

client_id = "1afc4f32b90641ae"
app_secret = "05f76e734610426bb47048cc497d6c35"
url = "https://member.bilibili.com/arcopen/fn/archive/add-by-utoken"
access_token_url = "https://api.bilibili.com/x/account-oauth2/v1/token"
refresh_token_url = "https://api.bilibili.com/x/account-oauth2/v1/refresh_token"
user_info_url = "https://member.bilibili.com/arcopen/fn/user/account/info"
video_init_url = "https://member.bilibili.com/arcopen/fn/archive/video/init"
video_frag_upload_url = "https://openupos.bilivideo.com/video/v2/part/upload"
video_upload_url = "https://openupos.bilivideo.com/video/v2/upload"
cover_upload_url = "https://member.bilibili.com/arcopen/fn/archive/cover/upload"
contribute_url = "https://member.bilibili.com/arcopen/fn/archive/add-by-utoken"

# 添加请求头，需要就传
header = {
    "Content-Type": "application/x-www-form-urlencoded"
}
json_header = {
    "Content-Type": "application/json"
}

def get_access_token(code):

    # 通过字典方式定义请求body
    data = {
        'client_id': client_id,
        'client_secret': app_secret,
        'grant_type': "authorization_code",
        'code': code
    }
    # 字典转换k1=v1 & k2=v2 模式
    data = parse.urlencode(data)
    # 请求方式
    content = requests.post(url=access_token_url, headers=header, data=data).text
    content = json.loads(content)
    print("conent",content)
    return content

def refresh_token(refresh_token):
    data = {
        'client_id': client_id,
        'client_secret': app_secret,
        'grant_type': "refresh_token",
        'refresh_token': refresh_token
    }
    data = parse.urlencode(data)
    # 请求方式
    content = requests.post(url=refresh_token_url, headers=header, data=data).text
    content = json.loads(content)
    return content

# 获取用户信息接口
def get_user_info(access_token):
    data = {
        'client_id': client_id,
        'access_token': access_token
    }
    # data = parse.urlencode(data)
    # 请求方式
    content = requests.get(url=user_info_url, params=data).text
    content = json.loads(content)
    return content

# 文件初始化接口
def video_init(access_token):

    data = {
        'name':"test.mp4",
        'utype':"1"
    }
    data = json.dumps(data)
    # data = parse.urlencode(data)
    # 请求方式
    url = video_init_url+"?client_id="+client_id+"&access_token="+access_token
    content = requests.post(url= url ,headers=json_header, data=data).text
    content = json.loads(content)
    upload_token = content['data']['upload_token']
    return upload_token

# 文件分片上传接口
def video_frag_upload(upload_token):

    # 请求方式
    data = get_object('video/2023-01-09 08:13:54/flower.mp4')
    url = video_frag_upload_url + "?upload_token=" + upload_token + "&part_number=" + str(1)
    content = requests.post(url=url, headers=json_header, data=data).text
    content = json.loads(content)
    print("content",content)
    return content

# 单个视频文件上传接口
def video_upload(upload_token,video_url):
    # 请求方式
    data = get_object(video_url)

    # data = open("/home/mocuili/data/enjoy/video/2023-01-09 08:13:54/flower.mp4", 'rb+')
    # 输出读取到的数据
    # data = data.read()
    # print(data.content_length)
    url = video_upload_url + "?upload_token=" + upload_token
    content = requests.post(url=url, headers=json_header, data=data).text
    content = json.loads(content)
    print("content",content)
    return content

# 封面上传接口
def cover_upload(access_token,cover_url):
    data = get_object(cover_url)
    files = {
        'file': data
    }
    # data = parse.urlencode(data)
    # 请求方式
    url = cover_upload_url+"?client_id="+client_id+"&access_token="+access_token
    content = requests.post(url= url, files=files).text
    content = json.loads(content)
    bi_cover_url = content['data']['url']
    print("bi_cover_url", bi_cover_url)
    return bi_cover_url

# 投稿接口
def contribute(access_token,upload_token,title,cover,tid,desc,tag):
    # 请求方式
    data = {
        'title': title,
        'cover': cover,
        'tid':tid,
        'no_reprint':0,
        'desc':desc,
        'tag':tag,
        'copyright':1
    }
    data = json.dumps(data)
    url = contribute_url + "?client_id="+ client_id +\
          "&access_token="+ access_token +\
          "&upload_token=" + upload_token
    content = requests.post(url=url, headers=json_header, data=data).text
    content = json.loads(content)
    return content


def contribute_process(video):
    print("开始投稿："+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    video_id = video.id
    platform_token = select_refresh_token("bilibili")
    access_token = platform_token.access_token

    # 视频初始化
    upload_token = video_init(access_token)

    # 上传单个小视频
    video_upload(upload_token, video.video_url)

    # 上传封面
    bi_cover_url = cover_upload(access_token, video.cover_url)

    # 投稿
    title = video.bilibili_title
    cover = bi_cover_url
    tid = video.bilibili_tid
    desc = video.description
    tag = video.tag
    contribute_result = contribute(access_token, upload_token, title, cover, tid, desc, tag)
    print("contribute_result", contribute_result)
    resource_id = contribute_result['data']['resource_id']

    # 投稿完成之后修改第三方id和投稿状态
    update_video_open_id_and_status(video_id, resource_id, 2)
    print("结束投稿："+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    return contribute_result

# def upload_video(title,cover,tid,no_reprint,desc,tag,copyright,source):
#
#     # 通过字典方式定义请求body
#     FormData = {"client_id": '',
#                 "access_token": '',
#                 "upload_token": 1,
#                 "title": title,
#                 "cover": cover,
#                 "tid": tid,
#                 "no_reprint": no_reprint,
#                 "desc": desc,
#                 "tag": tag,
#                 "copyright": copyright,
#                 "source": source}
#
#     # 字典转换k1=v1 & k2=v2 模式
#     data = parse.urlencode(FormData)
#
#     # 请求方式
#     content = requests.post(url=access_token_url, data=data,headers=header).text
#     content = json.loads(content)
#     print("content",content)



if __name__ == "__main__":

     # init = False
     #
     # if init is True:
     #     code = "ceaf8e3f01ba41aa8cfa2b62ca0c7379"
     #     content = access_token(code)
     # else:
     #     r_token = "ed16c85d530189c0800ade9eb002fa11"
     #     content = refresh_token(r_token)
     #
     # print(content)
     # access_token = content['data']['access_token']

     # user_info = get_user_info(token)

     access_token = "1bcd72151f73deeb2890464c22021911"

     # 视频初始化
     upload_token = video_init(access_token)

     # 上传单个小视频
     video_upload(upload_token)

     # 上传封面
     cover_upload(access_token)

     # 投稿
     title = "那些关于别离的文字"
     cover = "https://archive.biliimg.com/bfs/archive/14bdc569dc189431682f9c62f0af45836bdafdfd.png"
     tid = 124
     desc = "BGM：「露を吸う群」_増田俊郎.mp3"
     tag = "别离,心理,文字,句子,人文,心理学,离开,思念"
     contribute(access_token,upload_token,title,cover,tid,desc,tag)