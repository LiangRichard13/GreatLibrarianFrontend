# @Author: LiXiang
# @Time: 2023/11/2 14:57
# @version: 1.0
from .apis.apis_project import *
from .extensions import api
from App.apis.apis_user import *
from App.apis.apis_APIKey import *

# user用户类
api.add_resource(FindById, '/user/findById')
api.add_resource(Login, '/user/login/')
api.add_resource(LoginToken, '/user/isExpired/')
api.add_resource(Register, '/user/register/')
api.add_resource(UpdateUser, '/user/update/')
api.add_resource(GetSameNetUsers, '/user/getSameNetUsers/')
api.add_resource(AddFriendShip, '/user/addFriendShip/')

# configure类  管理APIKey
api.add_resource(APIKeyAdd, '/APIKey/add')
api.add_resource(APIKeyDelete, '/APIKey/delete')
api.add_resource(APIKeySearch, '/APIKey/search')

# Project项目类
api.add_resource(ProjectAdd, '/project/add')
api.add_resource(ProjectDelete, '/project/delete')
api.add_resource(ProjectUpdate, '/project/update')
api.add_resource(ProjectSearch, '/project/search')
