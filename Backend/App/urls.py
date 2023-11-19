# @Author: LiXiang
# @Time: 2023/11/2 14:57
# @version: 1.0

from .extensions import api
from App.apis.apis_user import *
from App.apis.apis_configure import *

# user用户类
api.add_resource(FindById, '/user/findById')
api.add_resource(Login, '/user/login/')
api.add_resource(LoginToken, '/user/isExpired/')
api.add_resource(Register, '/user/register/')
api.add_resource(UpdateUser, '/user/update/')

# configure类  管理APIKey
api.add_resource(APIKeyAdd, '/configure/APIKey/add')
api.add_resource(APIKeyDelete, '/configure/APIKey/delete')
api.add_resource(APIKeyUpdate, '/configure/APIKey/update')
api.add_resource(APIKeySearch, '/configure/APIKey/search')

# configure类  管理数据集
api.add_resource(DataSetAdd, '/configure/datasets/search')
api.add_resource(DataSetDelete, '/configure/datasets/delete')
api.add_resource(DataSetUpdate, '/configure/datasets/update')
api.add_resource(DataSetSearch, '/configure/datasets/search')
