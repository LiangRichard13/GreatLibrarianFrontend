# @Author:LiXiang
# @Time:2024/1/30 10:07
import ast
import os
import re

from datetime import datetime
from App.models import TestProject


def _backend_path():
    # 设置文件路径
    index = os.path.abspath(__file__).find('App')
    backend_path = os.path.abspath(__file__)[:index] if index != -1 else print("Backend not found")
    return backend_path


"""def add_code_to_class(file, addCode, className):
    try:
        template = os.path.join(_backend_path(), 'App', 'utils', 'config_template.py')  # 模板路径
        with open(template, 'r', encoding='utf-8') as f:
            content = f.read()  # 读取原文件内容
        start = content.find(f"class {className}(LLMs):")  # 定位要添加代码的类所在的位置
        if start == -1:
            return False
        end = content.find("\n", start)
        # 在类的合适位置插入新代码
        new_content = ("# @Creat File Time: " + datetime.now().strftime("%Y/%m/%d %H:%M") + "\n"
                       + content[:end] + f"\n{addCode}\n" + content[end:])
        os.makedirs(os.path.join('..', 'data', 'config', 'Temp'), exist_ok=True)  # 创建多层文件夹
        # 将修改后的内容写入新文件
        with open(file, 'w', encoding='utf-8') as new_file:
            new_file.write(new_content)
        compile(new_content, file, 'exec')  # 编译新文件以检查语法错误
        return True
    except SyntaxError as e:
        print(f"配置脚本文件发生语法错误：{e}")
        return False
    except Exception as e:
        print(f"发生了其他错误：{e}")
        return False"""


# 补充类的实例化参数
def update_instance(tPid):
    tp = TestProject.query.filter(TestProject.tP_id == tPid).first()
    temp_path = os.path.join(_backend_path(), 'App', 'data', 'config', 'Temp', 'config_' + tPid + '.py')  # 配置文件临时区路径

    # 参数值
    type_1 = "qwen_turbo"
    apikey_1 = "your_apikey_1"
    name_1 = "qwen_turbo_name"
    llm_intro_1 = "your_llm_intro_1"

    type_2 = "wenxin"
    ak_2 = "your_ak_2"
    sk_2 = "your_sk_2"
    name_2 = "wenxin_name"
    llm_intro_2 = "your_llm_intro_2"

    # 读取模板文件内容
    with open(temp_path, 'r', encoding='utf-8') as file:
        template_content = file.read()

    # 定义要替换的变量名
    variable_name_1 = "llm_cfg1"
    variable_name_2 = "llm_cfg2"

    # 构造替换的正则表达式
    pattern_1 = re.compile(rf'{variable_name_1}\s*=\s*dict\([^)]*\)', re.DOTALL)
    pattern_2 = re.compile(rf'{variable_name_2}\s*=\s*dict\([^)]*\)', re.DOTALL)

    # 替换模板中的值
    llm_cfg1_updated = pattern_1.sub(
        f'{variable_name_1} = dict(type="{type_1}", apikey="{apikey_1}", name="{name_1}", llm_intro="{llm_intro_1}")',
        template_content)
    llm_cfg2_updated = pattern_2.sub(
        f'{variable_name_2} = dict(type="{type_2}", ak="{ak_2}", sk="{sk_2}", name="{name_2}", llm_intro="{llm_intro_2}")',
        llm_cfg1_updated)
    try:
        # 写入更新后的内容到新文件
        with open(temp_path, 'w', encoding='utf-8') as output_file:
            output_file.write(llm_cfg2_updated)

        compile(llm_cfg2_updated, temp_path, 'exec')  # 编译新文件以检查语法错误
        return True
    except SyntaxError as e:
        print(f"配置脚本文件发生语法错误：{e}")
        return False
    except Exception as e:
        print(f"发生了其他错误：{e}")
        return False


def update_code_to_class(file_path, updated_code, class_name):
    with open(file_path, 'r', encoding='UTF-8') as file:
        code = file.read()

    # 解析代码为AST
    tree = ast.parse(code)
    try:
        # 遍历AST找到目标类
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                # 遍历类的成员找到__call__函数
                for class_node in node.body:
                    if isinstance(class_node, ast.FunctionDef) and class_node.name == '__call__':
                        # 替换__call__函数的代码块
                        class_node.body = ast.parse(updated_code).body[0].body
        updated_code = ast.unparse(tree)  # 重新生成代码
        with open(file_path, 'w', encoding='UTF-8') as file:
            file.write(updated_code)  # 将更新后的代码写回文件
        return True
    except SyntaxError as e:
        print(f"配置脚本文件发生语法错误：{e}")
        return False
    except Exception as e:
        print(f"发生了其他错误：{e}")
        return False


def add_call_function(file_path, updated_code, class_name):
    template = os.path.join(_backend_path(), 'App', 'utils', 'config_template.py')  # 模板路径
    with open(template, 'r', encoding='UTF-8') as file:
        file_code = file.read()
    # 解析代码为AST
    tree = ast.parse(file_code)

    # 遍历AST找到目标类
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            # 检查类中是否已经存在 __call__ 函数
            if not any(isinstance(member, ast.FunctionDef) and member.name == '__call__' for member in node.body):
                try:
                    new_call_ast = ast.parse(updated_code).body[0]  # 创建一个新的 __call__ 函数节点
                    node.body.append(new_call_ast)  # 将新的 __call__ 函数添加到类的成员中
                    new_content = ast.unparse(tree)  # 重新生成代码
                    os.makedirs(os.path.join(_backend_path(), 'App', 'data', 'config', 'Temp'), exist_ok=True)  # 创建文件夹
                    with open(file_path, 'w', encoding='UTF-8') as file:
                        file.write(new_content)  # 将更新后的代码写回文件
                    compile(new_content, file_path, 'exec')  # 编译新文件以检查语法错误
                    return True
                except SyntaxError as e:
                    print(f"配置脚本文件发生语法错误：{e}")
                    return False
                except Exception as e:
                    print(f"发生了其他错误：{e}")
                    return False
            else:
                print(f"Class '{class_name}' already has a __call__ function.")
            break

# update_code = """
# def __call__(self, prompt: str, history=None) -> str:
#     print("我是修改后的代码code-------------------")
#     return True
# """

# add_code = """
# def __call__(self, prompt: str, history=None) -> str:
#     print("我是修改后的代码code-------------------")
#     return True
# """

# config_path = os.path.join('..', 'data', 'config', 'config_test.py')  # 配置文件路径
# # print(update_code_to_class(config_path, update_code, "new_llm1"))
# temp_path = os.path.join('..', 'data', 'config', 'Temp', 'config_123.py')  # 配置文件临时区路径
# print(add_call_function(temp_path, add_code, "new_llm1"))
