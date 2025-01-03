#!/bin/bash

# 设置数据库和数据文件夹的路径
DATABASE_PATH="../Backend/instance/sqlite3.db"
DATA_FOLDER_PATH="../Backend/App/data"

# 显示操作提示信息
echo "Init your project.Clear all database data and static files."

# 确认用户是否要执行操作
read -p "Go ahead and delete it?(y/n): " choice
case "$choice" in 
  y|Y ) 
    # 用户选择了"是"，执行清空操作
    # 连接到SQLite数据库，并执行一个删除操作,清空以tb开头的表
    echo "clearing database data......"
    sqlite3 $DATABASE_PATH <<EOF
    $(echo "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'tb%';" | sqlite3 $DATABASE_PATH | awk '{print "DELETE FROM " $1 ";"}')
EOF

    # 检查data文件夹是否为空
    if [ "$(ls -A $DATA_FOLDER_PATH)" ]; then
        echo "clearing static files......"
        # 删除data文件夹下的所有内容
        rm -rf "$DATA_FOLDER_PATH"/*
    else
        echo "no static files to clear......"
    fi
    ;;
  n|N ) 
    # 用户选择了"否"，退出脚本
    echo "NO,Exit."
    ;;
  * ) 
    # 用户输入了无效的选项，提示错误并退出脚本
    echo "Invalid choices. Please input (y/n)"
    exit 1
    ;;
esac

# 提示用户按任意键退出
read -n 1 -s -r -p "按任意键退出..."
