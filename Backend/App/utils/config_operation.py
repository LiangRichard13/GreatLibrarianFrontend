# @Author:LiXiang
# @Time:2024/1/30 10:07
import ast
import os
import re

from datetime import datetime
from App.models import TestProject, APIKey
from App.utils.backend_path import BackendPath


# 补充类的实例化参数
def update_instance(tPid):
    tp = TestProject.query.filter(TestProject.tP_id == tPid).first()
    AK1 = APIKey.query.filter(APIKey.AK_id == tp.AK1).first()
    AK2 = APIKey.query.filter(APIKey.AK_id == tp.AK2).first()
    temp_path = os.path.join(BackendPath(), 'App', 'data', 'config', 'config_' + tPid + '.py')  # 配置文件临时区路径
    # 读取模板文件内容
    with open(temp_path, 'r', encoding='utf-8') as file:
        template_content = file.read()
    # 替换模板中的值
    llm_cfg1_updated = re.compile(rf'llm_cfg1\s*=\s*dict\([^)]*\)', re.DOTALL).sub(
        f'llm_cfg1 = dict(type="testLLM", apikey="{AK1.AK_value}",name="{AK1.AK_name}",'
        f' llm_intro="{"" if AK1.AK_intro is None else AK1.AK_intro}")', template_content)
    llm_cfg2_updated = re.compile(rf'llm_cfg2\s*=\s*dict\([^)]*\)', re.DOTALL).sub(
        f'llm_cfg2 = dict(type="evaluationLLM", apikey="{AK2.AK_value}", name="{AK2.AK_name}", '
        f'llm_intro="{"" if AK2.AK_intro is None else AK2.AK_intro}")', llm_cfg1_updated)
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


def add_call_function(file_path, flag, updated_code, class_name):
    template = file_path if flag == 1 else os.path.join(BackendPath(), 'App', 'utils', 'config_template_fin.py')  # 模板路径
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
                    if len(ast.parse(updated_code).body) != 0:
                        new_call_ast = ast.parse(updated_code).body[0]  # 创建一个新的 __call__ 函数节点
                        node.body.append(new_call_ast)  # 将新的 __call__ 函数添加到类的成员中
                        new_content = ast.unparse(tree)  # 重新生成代码
                        os.makedirs(os.path.join(BackendPath(), 'App', 'data', 'config', 'Temp'), exist_ok=True)
                        with open(file_path, 'w', encoding='UTF-8') as file:
                            file.write(new_content)  # 将更新后的代码写回文件
                        compile(new_content, file_path, 'exec')  # 编译新文件以检查语法错误
                        return True
                    else:
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
