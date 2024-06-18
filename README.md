##   项目介绍
### 项目概述

本项目是一个大模型测试平台，采用Vue.js和Flask构建的Web应用程序。该工具箱主要用于对大模型进行全面的性能评估。它支持多项测试功能，包括基础能力测试、幻觉测试和毒性测试，旨在提供一个综合的评估框架来衡量模型的表现。

### 主要功能

1. **API Key 配置**：用户可以配置一个或多个大模型的API Key，用于指定将要测试的模型。
2. **数据集配置**：允许用户为不同的测试选择并配置适当的数据集。
3. **基础能力测试**：在这一模块中，用户可以输入两个不同的API Key，其中一个用于执行测试，另一个用于评估测试结果，以对比和评估两个模型的性能。
4. **幻觉测试**：该测试旨在评估模型在面对非现实或虚构信息时的反应能力，识别模型是否产生不切实际的或逻辑不合理的输出。
5. **毒性测试**：专门设计来检测模型输出中的有害、有偏见或不当言论，以评估模型的安全性和公平性。
6. **协作功能**：支持局域网内用户之间的协作。用户需先添加好友，之后可以共同进行测试记录的审核，协作完成测试报告的迭代更新。
7. **报告下载**：用户可以下载测试过程中生成的多个迭代版本的测试报告。
8. **交互记录查看**：无论进行何种类型的测试，用户均能查看最终的交互记录，以便分析模型的响应和行为。

##   启动教程
### 开发环境要求
- **Node.js**: 必需，因为它包括了npm，npm是一个包管理工具，用于安装和管理前端项目的依赖。
- **Vue CLI**: 用于创建和管理Vue.js项目，是启动和开发Vue前端不可或缺的工具。可以通过npm安装。
- **Python 3**: 用于运行Flask后端。安装Python时通常会包括pip，pip是Python的包管理工具，用于安装Python依赖。
- **虚拟环境工具（推荐使用venv或conda）**: 用于创建隔离的Python环境，保持依赖的整洁和项目的独立性。当使用venv创建Python虚拟环境时，pip会自动被包含在环境中，无需单独安装。

### 项目结构

```
GreatLibrarianFrontend   项目根目录/
│
├── vue-frontend/            # Vue前端项目文件夹
│   ├── src/             # Vue源代码
│   ├── public/          # 静态资源
│   └── package.json     # 前端依赖配置文件
│
└── Backend/             # Flask后端项目文件夹
    ├── app.py           # Flask主应用文件
    └── requirements.txt # 后端依赖配置文件
```

### 安装步骤

#### 1. 克隆仓库

首先，克隆远程仓库到本地机器：

```
git clone [仓库URL]
cd [项目根目录]
```

#### 2. 设置后端环境

###### 使用Python虚拟环境

在项目的后端目录下创建一个Python虚拟环境，并激活它：

```
cd Backend
python -m venv venv
source venv/bin/activate  # 在Windows下使用 venv\Scripts\activate
```

你也可以通过pycharm等工具来可视化创建和激活项目所需要的Python虚拟环境

安装Flask及其他依赖：

```
pip install -r requirements.txt
```

###### 使用Conda环境

如果你更喜欢使用Conda来管理Python环境，可以按照以下步骤来配置：

```
cd Backend
conda create --name myenv python=3.11  # 创建一个名为myenv的新环境
conda activate myenv                 # 激活环境
pip install -r requirements.txt       # 安装依赖
```

请确保将 `myenv` 替换为你希望命名的环境名，且Python版本与你的项目兼容。

#### 3. 设置前端环境

安装了Node.js和npm后，可以使用以下命令安装Vue CLI：

```
npm install -g @vue/cli
# 或者使用yarn
yarn global add @vue/cli
```

在项目的前端目录下安装依赖：

```
cd ../vue-frontend
npm install  # 或使用 yarn install
```

#### 4.启动(两种方式)

##### 通过脚本初始化并启动

目中包含了两个脚本 `init.sh` 和 `start.sh`，分别用于初始化和启动项目。

###### 初始化项目

双击或在命令行运行 `init.sh` 脚本来清除任何旧的数据并准备项目环境：

```
./init.sh
```

###### 启动项目

完成初始化后，运行 `start.sh` 脚本以启动前后端服务器：

```
./start.sh
```

这两个脚本将自动处理所有设置和启动过程，简化了手动启动各个组件的步骤。

##### 手动启动

在vue-frontend中运行Vue开发服务器：

```
npm run serve  # 或使用 yarn serve
```

在虚拟环境激活的情况下，在Backend运行Flask应用：

```
python app.py
```

### 访问应用

打开浏览器，访问 `http://localhost:8080` 查看Vue前端页面，同时确保Flask后端服务在 `http://localhost:5000` 运行。
