# @Author:LiXiang
# @Time:2024/1/29 9:57

from datetime import datetime


def add_code_to_class(template, file, className, addCode):
    try:
        with open(template, 'r', encoding='utf-8') as f:
            content = f.read()  # 读取原文件内容
        start = content.find(f"class {className}(LLMs):")  # 定位要添加代码的类所在的位置
        if start == -1:
            print(f"not find class {className}")
            return False
        end = content.find("\n", start)
        # 在类的合适位置插入新代码
        new_content = ("# @Creat File Time: " + datetime.now().strftime("%Y/%m/%d %H:%M") + "\n"
                       + content[:end] + f"\n{addCode}\n" + content[end:])
        # 将修改后的内容写入新文件
        with open(file, 'w', encoding='utf-8') as new_file:
            new_file.write(new_content)
        compile(new_content, file, 'exec')  # 编译新文件以检查语法错误
        print("代码无语法错误，可以正常运行。")
        return True

    except SyntaxError as e:
        print(f"语法错误：{e}")
        return False

    except Exception as e:
        print(f"发生了其他错误：{e}")
        return False


# 设置文件路径
template_path = "config_template.py"
config_path = "config.py"

# 要添加代码的类名和代码
class_name = "new_llm1"
code = """
    def __call__(self, prompt: str, history=None) -> str:
        dashscope.api_key = self.apikey
        response = dashscope.Generation.call(
            model=dashscope.Generation.Models.qwen_turbo, prompt=prompt, history=history
        )

        if response:
            if response["output"]:
                if response["output"]["text"]:
                    return response["output"]["text"]
        return "API Problem"
"""

# 调用函数，生成新文件
result = add_code_to_class(template_path, config_path, class_name, code)

# 如果生成新文件成功，执行新文件的内容
# if result:
#     exec(open(new_file_path).read())
