import zhipuai

class new_llm:

    def __init__(self, apikey) -> None:
        self.apikey = apikey

    def __call__(self, prompt: str) -> str:
        return 'API Problem'

def checkllm(LLM) -> bool:
    result = LLM('你好')
    return isinstance(result, str) and result not in [None, 'API Problem']