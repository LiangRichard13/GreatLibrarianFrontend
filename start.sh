#!/bin/bash

getRoot() {
  # 获取当前目录并保存在变量GLF_Root下
  GLF_Root=$(pwd)

  # 输出变量GLF_Root以验证
  echo "The current directory is:：$GLF_Root"
  # 导出GLF_Root变量
  export GLF_Root
}
# 选择conda环境
select_conda_env() {
  echo "Retrieving all current conda environments:"
  env_list=$(conda env list | awk '{print $1}' | grep -v '^#') # 获取环境列表并排除注释行和路径行

  # 将环境列表转换为数组
  readarray -t envs <<<"$env_list"

  # 显示所有环境并提示用户输入
  echo "List of available conda environments:"
  for env in "${envs[@]}"; do
    echo "  - $env"
  done
  while true; do
    read -p "Please enter the name of the conda:" conda_env

    # 验证用户输入的环境是否存在
    if printf '%s\n' "${envs[@]}" | grep -qx "$conda_env"; then
      echo "The environment you selected is:$conda_env"
      export SELECTED_ENV="$conda_env" # 导出环境变量
      break                            # 如果输入有效，退出循环
    else
      echo "Error: No environment named '$conda_env' found, please enter a name from the list of environments shown."
    fi
  done
}

getRoot
select_conda_env # 选择conda环境

# 启动后端
#./Backend/venv/Scripts/python ./Backend/app.py &
cd Backend && python app.py &

# 启动前端
#cd vue-frontend && npm install && npm run serve &
cd vue-frontend && npm run serve &

# 无限循环以防止脚本结束
while true; do
  sleep 1
done
