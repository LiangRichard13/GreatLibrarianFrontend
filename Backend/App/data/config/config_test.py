from greatlibrarian.Core import LLMs, FinalScore
from greatlibrarian.Configs import ExampleConfig
from greatlibrarian.Utils import Registry
import dashscope
import qianfan
import zhipuai
LLM_base = Registry('LLMs')

@LLM_base.register_module('qwen_turbo')
class new_llm1(LLMs):

    def __init__(self, apikey, name, llm_intro) -> None:
        self.apikey = apikey
        self.name = name
        self.llm_intro = llm_intro

    def get_intro(self) -> str:
        return self.llm_intro

    def get_name(self) -> str:
        return self.name

    def __call__(self, prompt: str, history=None) -> str:
        print('我是修改后的代码code-------------------')
        return True

@LLM_base.register_module('wenxin')
class new_llm2(LLMs):

    def __init__(self, ak, sk, name, llm_intro) -> None:
        self.ak = ak
        self.sk = sk
        self.name = name
        self.llm_intro = llm_intro

    def get_intro(self) -> str:
        return self.llm_intro

    def get_name(self) -> str:
        return self.name

    def __call__(self, prompt: str) -> str:
        chat_comp = qianfan.ChatCompletion(ak=self.ak, sk=self.sk)
        resp = chat_comp.do(model='ERNIE-Bot', messages=[{'role': 'user', 'content': prompt}])
        if resp:
            if resp['body']:
                if resp['body']['result']:
                    return resp['body']['result']
        return 'API Problem'