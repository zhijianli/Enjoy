import requests
import json

# 替换 YOUR_API_KEY 为你的 OpenAI API 密钥
api_key = "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"
headers = {"Authorization": f"Bearer {api_key}"}

# 定义 API 请求的数据
data = {
    "model": "text-davinci-002",  # 使用你喜欢的模型，例如 "text-davinci-002"
    "prompt": "Once upon a time",  # 替换为你想要的提示
    "max_tokens": 100,  # 生成的文本长度
    "n": 1,  # 生成的文本数量
    "stop": None,  # 用于指定结束序列的字符串，如["\n"]。
    "temperature": 1.0,  # 控制生成文本的随机性
}

# 发送请求到 OpenAI API
url = "https://api.openai.com/v1/engines/text-davinci-002/completions"
response = requests.post(url, headers=headers, json=data)

# 检查响应状态
if response.status_code == 200:
    response_json = response.json()
    generated_text = response_json["choices"][0]["text"]
    print("Generated text:", generated_text)
else:
    print("Error:", response.status_code, response.text)
