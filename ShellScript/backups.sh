#!/bin/bash

# 设置 Python 脚本路径
PYTHON_SCRIPT="backups.py" # Python 脚本的路径

cd ../Backend/App/utils && python "$PYTHON_SCRIPT"

# 提示用户按任意键退出
read -n 1 -s -r -p "按任意键退出..."
echo  # 输出换行
