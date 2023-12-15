# @Author: LiXiang
# @Time: 2023/11/2 14:57
# @version: 1.0

from .extensions import api
from App.apis.apis_user import *
from App.apis.apis_APIKey import *
from App.apis.apis_dataSet import *
from App.apis.apis_friend import *
from App.apis.apis_project import *

# user用户类
api.add_resource(FindById, '/user/findById')
api.add_resource(Login, '/user/login')
api.add_resource(LoginOut, '/user/loginOut')
api.add_resource(LoginToken, '/user/isExpired')
api.add_resource(Register, '/user/register')
api.add_resource(UpdateUser, '/user/update')
api.add_resource(GetUserList, '/user/getUserList')
api.add_resource(Icon, '/user/icon')

# 好友关系业务处理
api.add_resource(Friend, '/friend')

# configure类  管理APIKey
api.add_resource(APIKeyOperation, '/APIKey')

# Project项目类
api.add_resource(ProjectOperation, '/project')

# DataSet数据集类
api.add_resource(DataSetOperation, '/dataSet')
