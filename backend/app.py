from flask import Flask, request, jsonify  # 导入Flask框架和相关模块
from flask_sqlalchemy import SQLAlchemy  # 导入SQLAlchemy，用于数据库操作
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity  # 导入JWT模块，处理用户认证
from flask_cors import CORS  # 导入CORS，允许跨域请求
from model import db
from routes import bp
from chat import chat,socketio

app = Flask(__name__)  # 创建Flask应用
CORS(app)  # 允许所有域名进行跨域请求

# 配置数据库连接，使用MySQL数据库，用户名是root，密码是123123，数据库名是demo
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123123@localhost/demo'
# 配置JWT密钥，使用该密钥签发和验证JWT
app.config['JWT_SECRET_KEY'] = 'your_secret_key'

# 初始化数据库和JWT管理器
db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(bp)  # 注册蓝图
app.register_blueprint(chat) 

socketio.init_app(app)

# 主程序入口
if __name__ == '__main__':
    # 在应用程序上下文中创建数据库表
    with app.app_context():
        db.drop_all() # 删除数据库表
        db.create_all()  # 创建数据库表
    # 启动应用程序，开启调试模式
    socketio.run(app)
