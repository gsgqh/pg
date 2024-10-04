from flask import Flask, request, jsonify  # 导入Flask框架和相关模块
from flask_sqlalchemy import SQLAlchemy  # 导入SQLAlchemy，用于数据库操作
from flask_jwt_extended import JWTManager, create_access_token, jwt_required  # 导入JWT模块，处理用户认证
from flask_cors import CORS  # 导入CORS，允许跨域请求

app = Flask(__name__)  # 创建Flask应用
CORS(app)  # 允许所有域名进行跨域请求

# 配置数据库连接，使用MySQL数据库，用户名是root，密码是123qwe，数据库名是demo
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123qwe@localhost/demo'
# 配置JWT密钥，使用该密钥签发和验证JWT
app.config['JWT_SECRET_KEY'] = 'your_secret_key'

# 初始化数据库和JWT管理器
db = SQLAlchemy(app)
jwt = JWTManager(app)

# 定义用户模型，继承自SQLAlchemy的Model类
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 用户ID，主键
    username = db.Column(db.String(80), unique=True, nullable=False)  # 用户名，唯一且不能为空
    password = db.Column(db.String(200), nullable=False)  # 密码，不能为空

# 定义项目模型，继承自SQLAlchemy的Model类
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 项目ID，主键
    title = db.Column(db.String(200), nullable=False)  # 项目标题，不能为空
    content = db.Column(db.Text, nullable=False)  # 项目内容，不能为空

# 注册用户接口，接收POST请求
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # 获取请求体中的JSON数据
    # 创建新用户对象
    new_user = User(username=data['username'], password=data['password'])
    # 将新用户添加到数据库会话
    db.session.add(new_user)
    # 提交会话，保存用户到数据库
    db.session.commit()
    # 返回成功信息和状态码201
    return jsonify(message="User created"), 201

# 登录接口，接收POST请求
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # 获取请求体中的JSON数据
    # 查询数据库，查找与用户名和密码匹配的用户
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    if user:
        # 如果用户存在，创建JWT访问令牌
        access_token = create_access_token(identity=user.id)
        # 返回访问令牌
        return jsonify(access_token=access_token)
    # 如果用户不存在，返回认证失败信息和状态码401
    return jsonify(message="Bad credentials"), 401

# 创建项目接口，接收POST请求，要求JWT认证
@app.route('/create-project', methods=['POST'])
@jwt_required()  # 该路由需要JWT令牌验证
def create_project():
    data = request.get_json()  # 获取请求体中的JSON数据
    # 创建新项目对象
    new_project = Project(title=data['title'], content=data['content'])
    # 将新项目添加到数据库会话
    db.session.add(new_project)
    # 提交会话，保存项目到数据库
    db.session.commit()
    # 返回成功信息和状态码201
    return jsonify(message="Project created"), 201

# 获取所有项目接口，接收GET请求
@app.route('/projects', methods=['GET'])
def get_projects():
    # 查询数据库中的所有项目
    projects = Project.query.all()
    # 将项目列表转化为JSON格式并返回
    return jsonify([{'id': p.id, 'title': p.title, 'content': p.content} for p in projects])

# 主程序入口
if __name__ == '__main__':
    # 在应用程序上下文中创建数据库表
    with app.app_context():
        db.create_all()  # 创建数据库表
    # 启动应用程序，开启调试模式
    app.run(debug=True)
