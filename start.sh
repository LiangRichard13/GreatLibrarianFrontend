#!/bin/bash

# 获取当前目录并保存在变量GLF_Root下
GLF_Root=$(pwd)

# 输出变量GLF_Root以验证
echo "当前目录是：$GLF_Root"
# 导出GLF_Root变量
export GLF_Root

# 启动后端
./Backend/venv/Scripts/python ./Backend/app.py &

# 启动前端
cd vue-frontend && npm run serve &

# 无限循环以防止脚本结束
while true; do
    sleep 1
done