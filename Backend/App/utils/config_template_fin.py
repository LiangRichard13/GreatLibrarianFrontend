from greatlibrarian.Core import LLMs, FinalScore
from greatlibrarian.Configs import ExampleConfig
from greatlibrarian.Utils import Registry
import dashscope
import qianfan
import zhipuai

LLM_base = Registry("LLMs")


@LLM_base.register_module("chatglm")
class new_llm1(LLMs):
    def __init__(self, apikey, name, llm_intro) -> None:
        self.apikey = apikey
        self.name = name
        self.llm_intro = llm_intro

    def get_intro(self) -> str:
        return self.llm_intro

    def get_name(self) -> str:
        return self.name


@LLM_base.register_module("glm-3-turbo")
class new_llm2(LLMs):
    def __init__(self, apikey, name, llm_intro) -> None:
        self.apikey = apikey
        self.name = name
        self.llm_intro = llm_intro

    def get_intro(self) -> str:
        return self.llm_intro

    def get_name(self) -> str:
        return self.name


llm_cfg1 = dict(
    type="",
    apikey="",
    name="",
    llm_intro=""
)
chat = LLM_base.build(llm_cfg1)

llm_cfg2 = dict(
    type="",
    apikey="",
    name="",
    llm_intro=""
)
glm_3_turbo = LLM_base.build(llm_cfg2)
config4 = ExampleConfig(chat, glm_3_turbo)

config = config4
