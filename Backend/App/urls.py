# @Author: LiXiang
# @Time: 2023/11/2 14:57
# @version: 1.0

from .extensions import api
from App.apis.apis_user import *
from App.apis.apis_friend import *
from App.apis.apis_APIKey import *
from App.apis.apis_dataSet import *

from App.apis.apis_project import *
from App.apis.apis_projectAPIKey import *
from App.apis.apis_projectDataSet import *

from App.apis.apis_testProject import *
from App.apis.apis_testProjectOperation import *
from App.apis.apis_testProjectUser import *
from App.apis.apis_QA import *
from App.apis.apis_progress import *

# user用户类
api.add_resource(FindById, '/user/findById')
api.add_resource(Login, '/user/login')
api.add_resource(LoginOut, '/user/loginOut')
api.add_resource(LoginToken, '/user/isExpired')
api.add_resource(Register, '/user/register')
api.add_resource(UpdateUser, '/user/updateUser')
api.add_resource(UpdatePassWord, '/user/updatePassword')
api.add_resource(GetUserList, '/user/getUserList')
api.add_resource(Icon, '/user/icon')

# 好友关系业务处理
api.add_resource(Friend, '/friend')

# 管理APIKey
api.add_resource(APIKeyCRUD, '/APIKey')
# 管理DataSet数据集类
api.add_resource(DataSetCRUD, '/dataSet')

# Project项目类
api.add_resource(ProjectCRUD, '/project')
# 项目下管理APIKey
api.add_resource(ProjectAK, '/projectAK')
# 项目下管理DataSet
api.add_resource(ProjectDS, '/projectDS')

# testProject实验
api.add_resource(TestProjectCRUD, '/testProject')
# 实验操作
api.add_resource(testProjectOperation, '/testProjectOperation')
# 实现--协作者
api.add_resource(TestProjectUserCRUD, '/testProjectUser')

# 人工审核
api.add_resource(QAOperation, '/QA')
# 进度条
api.add_resource(Progress, '/progress')
