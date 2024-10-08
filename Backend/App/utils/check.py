import dashscope
import openai
from openai import OpenAI
import qianfan
import zhipuai
from zhipuai import ZhipuAI
from openai import OpenAI
import os
from llamaapi import LlamaAPI
from typing import Dict

class new_llm:

    def __init__(self, apikey) -> None:
        self.apikey = apikey

    def __call__(self, prompt: str) -> str:
        print('测试模型：gpt-4o')
        try:
            os.environ['OPENAI_API_KEY'] = self.apikey
            client = OpenAI()
            response = client.chat.completions.create(model='gpt-4o', messages=[{'role': 'user', 'content': prompt}], temperature=0.7, max_tokens=150)
            return response.choices[0].message.content
        except Exception as e:
            return f'API Problem: {e}'

def checkllm(LLM) -> bool:
    result = LLM('你好')
    return isinstance(result, str) and result not in [None, 'API Problem']