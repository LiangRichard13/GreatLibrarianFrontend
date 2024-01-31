# @Author: LiXiang
# @Time: 2023/11/2 14:57
# @version: 1.0

from .extensions import api

from App.apis import (user, friend, APIKey, dataSet, project, projectAPIKey, projectDataSet, testProject,
                      testProjectOperation, testProjectUser, QA, progress)

resources = [
    (user.UserCRUD, '/user'),  # user用户类
    (user.Login, '/user/login'),  # 登录操作
    (user.GetUserList, '/user/getUserList'),  # 获取用户列表
    (user.Icon, '/user/icon'),  # icon操作

    (friend.Friend, '/friend'),  # 好友关系业务处理

    (APIKey.APIKeyCRUD, '/APIKey'),  # 管理APIKey
    (dataSet.DataSetCRUD, '/dataSet'),  # 管理DataSet数据集类

    (project.ProjectCRUD, '/project'),  # Project项目类
    (projectAPIKey.ProjectAK, '/projectAK'),  # 项目下管理APIKey
    (projectDataSet.ProjectDS, '/projectDS'),  # 项目下管理DataSet

    (testProject.TestProjectCRUD, '/testProject'),  # testProject实验
    (testProject.ConfigCRUD, '/testProjectConfig'),  # 实验配置文件管理
    (testProjectOperation.TPOperation, '/testProjectOperation'),  # 实验操作
    (testProjectUser.TestProjectUserCRUD, '/testProjectUser'),  # 实现--协作者
    (QA.QAOperation, '/QA'),  # 人工审核
    (progress.Progress, '/progress')  # 进度条
]

for resource, url in resources:
    api.add_resource(resource, url)
