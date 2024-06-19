import zhipuai


class new_llm:

    def __init__(self, apikey) -> None:
        self.apikey = apikey

    def __call__(self, prompt: str) -> str:
        zhipuai.api_key = self.apikey
        response = zhipuai.model_api.invoke(model='chatglm_pro', prompt=[{'role': 'user', 'content': prompt}],
                                            top_p=0.7, temperature=0.9)
        if response:
            if response['code'] == 200:
                return response['data']['choices'][0]['content']
        else:
            return 'API Problem'


def checkllm(LLM) -> bool:
    result = LLM('你好')
    return isinstance(result, str) and result not in [None, 'API Problem']
