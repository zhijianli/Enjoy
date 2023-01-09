import requests
import json
from urllib import parse

client_id = "1afc4f32b90641ae"
app_secret = "05f76e734610426bb47048cc497d6c35"
url = "https://member.bilibili.com/arcopen/fn/archive/add-by-utoken"
access_token_url = "https://api.bilibili.com/x/account-oauth2/v1/token"
refresh_token_url = "https://api.bilibili.com/x/account-oauth2/v1/refresh_token"
user_info_url = "https://member.bilibili.com/arcopen/fn/user/account/info"
video_init_url = "https://member.bilibili.com/arcopen/fn/archive/video/init"

# 添加请求头，需要就传
header = {
    "Content-Type": "application/x-www-form-urlencoded"
}
json_header = {
    "Content-Type": "application/json"
}

def access_token(code):

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

def video_init(access_token):
    data = {
        'client_id': client_id,
        'access_token': access_token
    }
    # data = json.dumps(data)
    data = parse.urlencode(data)
    # 请求方式
    content = requests.post(url=video_init_url,headers=header, data=data).text
    content = json.loads(content)
    return content


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


def upload_video(title,cover,tid,no_reprint,desc,tag,copyright,source):

    # 通过字典方式定义请求body
    FormData = {"client_id": '',
                "access_token": '',
                "upload_token": 1,
                "title": title,
                "cover": cover,
                "tid": tid,
                "no_reprint": no_reprint,
                "desc": desc,
                "tag": tag,
                "copyright": copyright,
                "source": source}

    # 字典转换k1=v1 & k2=v2 模式
    data = parse.urlencode(FormData)

    # 请求方式
    content = requests.post(url=access_token_url, data=data,headers=header).text
    content = json.loads(content)
    print("content",content)



if __name__ == "__main__":

     init = True

     if init is True:
         code = "ceaf8e3f01ba41aa8cfa2b62ca0c7379"
         content = access_token(code)
     else:
         r_token = "8aae5c4800213312ef662b23036f4c11"
         content = refresh_token(r_token)

     print(content)
     token = content['data']['access_token']

     user_info = get_user_info(token)
     print("user_info",user_info)

     init_info = video_init(token)
     print("init_info", init_info)