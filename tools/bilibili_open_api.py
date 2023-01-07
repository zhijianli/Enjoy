import requests
import json
from urllib import parse

client_id = "1afc4f32b90641ae"
app_secret = "05f76e734610426bb47048cc497d6c35"
url = "https://member.bilibili.com/arcopen/fn/archive/add-by-utoken"
access_token_url = "https://api.bilibili.com/x/account-oauth2/v1/token"

# 添加请求头，需要就传
header = {
    "Content-Type": "application/x-www-form-urlencoded"
}


def access_token(code):
    # 通过字典方式定义请求body
    FormData = {"client_id": client_id,
                "client_secret": app_secret,
                "grant_type": "authorization_code",
                "code": code}
    # 字典转换k1=v1 & k2=v2 模式
    data = parse.urlencode(FormData)

    # 请求方式
    content = requests.post(url=url, headers=header, data=data).text
    content = json.loads(content)
    print(content)


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
    content = requests.post(url=access_token_url, headers=header, data=data).text
    content = json.loads(content)
    print("content",content)



if __name__ == "__main__":
    # title = ''
    # cover = ''
    # tid = ''
    # no_reprint = ''
    # desc = ''
    # tag = ''
    # copyright = ''
    # source = ''
    #
    # upload_video(title,cover,tid,no_reprint,desc,tag,copyright,source)

    access_token()