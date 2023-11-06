# @Author: LiXiang
# @Time: 2023/11/2 14:57
# @version: 1.0

import app
from .extensions import api
from .apis import *

api.add_resource(FindById, '/user/findById')
api.add_resource(Login, '/user/login/')
api.add_resource(LoginToken, '/user/isExpired/')
api.add_resource(Register, '/user/register/')
