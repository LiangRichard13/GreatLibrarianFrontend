import dashscope
import openai
import requests
from openai import OpenAI
import qianfan
import zhipuai
from zhipuai import ZhipuAI
from openai import OpenAI
import os
from llamaapi import LlamaAPI
from typing import Dict
import requests


class new_llm:

    def __init__(self, apikey) -> None:
        self.apikey = apikey

    def __call__(self, prompt: str, history: list = None) -> str:
        print("-------------------call-------------------")


def checkllm(LLM) -> bool:
    result = LLM('你好')
    print(result)
    return isinstance(result, str) and 'API Problem' not in result
