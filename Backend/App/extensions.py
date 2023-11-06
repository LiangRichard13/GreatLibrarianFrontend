# @Author: LiXiang
# @Time: 2023/11/2 14:57
# @version: 1.0
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

db = SQLAlchemy()
migrate = Migrate()
api = Api()


def init_extensions(app):
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    api.init_app(app=app)
