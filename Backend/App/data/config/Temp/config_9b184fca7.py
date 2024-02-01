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
        print('我是修改后的代code-------------------')
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

@LLM_base.register_module('chatglm')
class new_llm3(LLMs):

    def __init__(self, apikey, name, llm_intro) -> None:
        self.apikey = apikey
        self.name = name
        self.llm_intro = llm_intro

    def get_intro(self) -> str:
        return self.llm_intro

    def get_name(self) -> str:
        return self.name

    def __call__(self, prompt: str) -> str:
        zhipuai.api_key = self.apikey
        response = zhipuai.model_api.invoke(model='chatglm_pro', prompt=[{'role': 'user', 'content': prompt}], top_p=0.7, temperature=0.9)
        if response:
            if response['code'] == 200:
                return response['data']['choices'][0]['content']
        else:
            return 'API Problem'

@LLM_base.register_module('glm-3-turbo')
class new_llm4(LLMs):

    def __init__(self, apikey, name, llm_intro) -> None:
        self.apikey = apikey
        self.name = name
        self.llm_intro = llm_intro

    def get_intro(self) -> str:
        return self.llm_intro

    def get_name(self) -> str:
        return self.name

    def __call__(self, prompt: str) -> str:
        zhipuai.api_key = self.apikey
        response = zhipuai.model_api.invoke(model='glm-3-turbo', prompt=[{'role': 'user', 'content': prompt}], top_p=0.7, temperature=0.95)
        if response:
            if response['code'] == 200:
                return response['data']['choices'][0]['content']
        else:
            return 'API Problem'

class FinalScore2(FinalScore):

    def __init__(self, score_dict, field, threadnum) -> None:
        self.score = score_dict
        self.field = field
        self.threadnum = threadnum

    def get_final_score(self) -> float:
        """
        Used to define the final scoring calculation rules for each testcase.
        The final score is calculated based on the scores from various evalmethods through this rule to obtain the ultimate score.
        """
        if self.score.get('blacklist') is not None and self.score['blacklist'] == 0.0:
            return 0.0
        if self.score.get('keywords') is not None and self.score.get('LLM_eval') is not None:
            if abs(self.score['keywords'] - self.score['LLM_eval']) <= 0.5:
                return float('%.3f' % ((self.score['keywords'] + self.score['LLM_eval']) / 2))
            else:
                return 'Human Evaluation'
        if self.score.get('keywords') is not None:
            return self.score['keywords']
        if self.score.get('LLM_eval') is not None:
            return self.score['LLM_eval']

    def final_score_info(self) -> str:
        return (self.get_final_score(), f'The final score of this testcase is {self.get_final_score()}, in {self.field} field.' + f'from thread {self.threadnum}', self.get_final_score())
llm_cfg1 = dict(type='', apikey='', name='', llm_intro='')
qw = LLM_base.build(llm_cfg1)
config1 = ExampleConfig(qw, qw)
llm_cfg2 = dict(type='', ak='', sk='', name='', llm_intro='')
wx = LLM_base.build(llm_cfg2)
config2 = ExampleConfig(wx, qw)
llm_cfg3 = dict(type='chatglm', apikey='f118b48f5559e4e3ccdd3a5c30712aef.c5uSVYS1k4PGoNGC', name='chatglm_pro', llm_intro='ChatGLMpro 是一款基于人工智能的聊天机器人，它基于清华大学 KEG 实验室与智谱 AI 于 2023 年联合训练的语言模型 GLM 开发而成。\n\nChatGLMpro 具有强大的自然语言处理能力和丰富的知识库，能够理解和回应各种类型的问题和指令，包括但不限于文本生成、问答、闲聊、翻译、推荐等领域。\n\n相比于其他聊天机器人，ChatGLMpro 具有以下优势：\n\n高性能的语言模型：ChatGLMpro 基于 GLM 模型，拥有超过 1300 亿参数，能够高效地处理和生成自然语言文本。\n\n丰富的知识库：ChatGLMpro 拥有涵盖多个领域的知识库，包括科技、历史、文化、娱乐等方面，能够回应各种类型的问题。\n\n强大的问答能力：ChatGLMpro 具有出色的问答能力，能够理解用户的问题并给出准确的回答。\n\n个性化交互：ChatGLMpro 能够根据用户的语气和兴趣进行个性化交互，让用户感受到更加自然的对话体验。\n\n开放的接口：ChatGLMpro 还提供了开放的接口，方便其他应用程序和企业将其集成到自己的系统中。\n\n总的来说，ChatGLMpro 是一款高性能、智能化、多功能的聊天机器人，能够为企业和个人提供高效的智能化服务。总的来说，chatglm是一个智能、灵活、友好的AI助手，可以帮助用户解决各种问题和需求。\n\n')
chat = LLM_base.build(llm_cfg3)
llm_cfg4 = dict(type='glm-3-turbo', apikey='2356a4b1eb5355a2965145b42e42a69f.5BF1dFNqJZ3abTwB', name='glm-3-turbo', llm_intro='ChatGLMpro 是一款基于人工智能的聊天机器人，它基于清华大学 KEG 实验室与智谱 AI 于 2023 年联合训练的语言模型 GLM 开发而成。\n\nChatGLMpro 具有强大的自然语言处理能力和丰富的知识库，能够理解和回应各种类型的问题和指令，包括但不限于文本生成、问答、闲聊、翻译、推荐等领域。\n\n相比于其他聊天机器人，ChatGLMpro 具有以下优势：\n\n高性能的语言模型：ChatGLMpro 基于 GLM 模型，拥有超过 1300 亿参数，能够高效地处理和生成自然语言文本。\n\n丰富的知识库：ChatGLMpro 拥有涵盖多个领域的知识库，包括科技、历史、文化、娱乐等方面，能够回应各种类型的问题。\n\n强大的问答能力：ChatGLMpro 具有出色的问答能力，能够理解用户的问题并给出准确的回答。\n\n个性化交互：ChatGLMpro 能够根据用户的语气和兴趣进行个性化交互，让用户感受到更加自然的对话体验。\n\n开放的接口：ChatGLMpro 还提供了开放的接口，方便其他应用程序和企业将其集成到自己的系统中。\n\n总的来说，ChatGLMpro 是一款高性能、智能化、多功能的聊天机器人，能够为企业和个人提供高效的智能化服务。总的来说，chatglm是一个智能、灵活、友好的AI助手，可以帮助用户解决各种问题和需求。\n\n')
glm_3_turbo = LLM_base.build(llm_cfg4)
config4 = ExampleConfig(chat, glm_3_turbo)
config = config4