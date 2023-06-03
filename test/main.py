import asyncio
import openai
import functools

def create_chat_completion(session, chat_model):
    response = openai.ChatCompletion.create(
        model= chat_model,  # 对话模型的名称
        messages=session,
        max_tokens=500,
        stream=True  # this time, we set stream=True
    )
    return response

async def main(session, chat_model):
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, functools.partial(create_chat_completion, session, chat_model))
    chat_text = ''
    for chunk in response:
        chunk_message = chunk['choices'][0]['delta']  # extract the message
        if 'content' not in chunk_message:
            continue
        # res['data'] = chunk_message['content']
        # res['state'] = 'continue'
        #
        # data = await self.send(websocket, res)
        # if data['cmd'] == 'stop':
        #     # response.clear()
        #     response = ""
        #     break
        #
        # chat_text += res['data']
        chat_text += chunk_message['content']
        print(chat_text)


openai.api_key = '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'

# 创建一个聊天会话
session = [{'role': 'system', 'content': '你是一个文案写手.'}, {'role': 'user', 'content': '写一篇关于佛学的微信公众号文章'}]
chat_model = 'gpt-3.5-turbo'

# 使用事件循环异步调用 main 方法
asyncio.run(main(session, chat_model))







