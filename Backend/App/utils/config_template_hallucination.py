from greatlibrarian.Core import LLMs, FinalScore
from greatlibrarian.Configs import ExampleConfig
from greatlibrarian.Utils import Registry
import dashscope
import qianfan
import zhipuai
import requests

LLM_base = Registry("LLMs")


@LLM_base.register_module("testLLM")
class new_llm1(LLMs):
    def __init__(self, apikey, name, llm_intro) -> None:
        self.apikey = apikey
        self.name = name
        self.llm_intro = llm_intro

    def get_intro(self) -> str:
        return self.llm_intro

    def get_name(self) -> str:
        return self.name


@LLM_base.register_module("mix")
class new_llm2(LLMs):
    def __init__(self, name, llm_intro) -> None:
        self.name = name
        self.llm_intro = llm_intro

    def __call__(self, prompt: str) -> str:
        response = requests.post(url="http://192.168.71.80:8888/", json={"prompt": prompt})
        try:
            status = response.status_code
            if status == 200:
                return eval(response.content)["response"]
            else:
                return "API Problem"
        except:
            return "API Problem"


llm_cfg1 = dict(
    type="",
    apikey="",
    name="",
    llm_intro=""
)
testLLM = LLM_base.build(llm_cfg1)

llm_cfg2 = dict(
    type="mix",
    name="mix",
    llm_intro=''
)
mix = LLM_base.build(llm_cfg2)
config5 = ExampleConfig(testLLM, mix)
config = config5
