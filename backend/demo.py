from flask import Flask, request, jsonify  # 导入Flask框架和相关模块
from flask_sqlalchemy import SQLAlchemy  # 导入SQLAlchemy，用于数据库操作
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity  # 导入JWT模块，处理用户认证
from flask_cors import CORS  # 导入CORS，允许跨域请求
from flask_login import current_user, login_required  # 使用 Flask-Login 进行用户管理


app = Flask(__name__)  # 创建Flask应用
CORS(app)  # 允许所有域名进行跨域请求

# 配置数据库连接，使用MySQL数据库，用户名是root，密码是123123，数据库名是demo
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123123@localhost/demo'
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
    nickname = db.Column(db.String(100))  # 用户昵称
    gender = db.Column(db.String(10))  # 性别，值可以是 'male', 'female' 等
    birthday = db.Column(db.Date)  # 生日，使用日期类型
    signature = db.Column(db.String(200))  # 签名
    school = db.Column(db.String(200))  # 学校名称
    major = db.Column(db.String(100))  # 专业
    interests = db.Column(db.Text)  # 兴趣，文本类型，可以存储多个兴趣

# 定义项目模型，继承自SQLAlchemy的Model类
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 项目ID，主键
    title = db.Column(db.String(200), nullable=False)  # 项目标题，不能为空
    content = db.Column(db.Text, nullable=False)  # 项目内容，不能为空
    username = db.Column(db.String(80), nullable=False)  # 当前创建项目的用户的用户名，不能为空

# 注册用户接口，接收POST请求
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # 获取请求体中的JSON数据

    # 检查用户名是否已存在
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify(message="Username already exists", success=False), 200

    # 检查昵称是否为空
    if not data.get('nickname'):
        return jsonify(message="Nickname cannot be empty", success=False), 200

    # 创建新用户对象，包含昵称
    new_user = User(username=data['username'], password=data['password'], nickname=data['nickname'])
    
    # 将新用户添加到数据库会话
    db.session.add(new_user)
    # 提交会话，保存用户到数据库
    db.session.commit()

    # 返回成功信息和状态码201
    return jsonify(message="User created", success=True), 201


# 登录接口，接收POST请求
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # 获取请求体中的JSON数据
    # 查询数据库，查找与用户名匹配的用户
    user = User.query.filter_by(username=data['username']).first()
    
    if user:
        # 如果用户存在，检查密码
        if user.password == data['password']:
            # 密码正确，创建JWT访问令牌
            access_token = create_access_token(identity=user.id)
            # 返回访问令牌
            return jsonify(access_token=access_token,success=True), 200  # 返回200状态码
        else:
            # 密码错误，返回相应消息
            return jsonify(message="Incorrect password",success=False), 200  # 返回200状态码
    else:
        # 用户不存在，返回相应消息
        return jsonify(message="User does not exist",success=False), 200  # 返回200状态码


# 创建项目接口，接收POST请求，要求JWT认证
@app.route('/create-project', methods=['POST'])
@jwt_required()  # 该路由需要JWT令牌验证
def create_project():
    data = request.get_json()  # 获取请求体中的JSON数据

    # 检查标题和内容是否为空
    if not data.get('title') or not data.get('content'):
        return jsonify(message="Title or content cannot be empty", success = False), 200  # 返回200状态码

    # 获取当前用户的身份信息
    current_user_id = get_jwt_identity()
    
    # 查询当前用户以获取用户名
    user = User.query.get(current_user_id)
    if not user:
        return jsonify(message="User not found",success = False), 200  # 如果找不到用户，返回200

    # 创建新项目对象，保存用户名
    new_project = Project(title=data['title'], content=data['content'], username=user.username)
    
    # 将新项目添加到数据库会话
    db.session.add(new_project)
    # 提交会话，保存项目到数据库
    db.session.commit()
    
    # 返回成功信息和状态码201
    return jsonify(message="Project created", success = True), 201

# 获取所有项目接口，接收GET请求
@app.route('/projects', methods=['GET'])
def get_projects():
    # 查询数据库中的所有项目
    projects = Project.query.all()

    # 为每个项目找到对应用户的 nickname
    project_list = []
    for project in projects:
        # 通过 username 查询对应的 User 表中的 nickname
        user = User.query.filter_by(username=project.username).first()
        nickname = user.nickname if user else None  # 如果找不到用户，nickname 为 None

        # 构建项目和用户的 JSON 数据
        project_list.append({
            'id': project.id,
            'title': project.title,
            'content': project.content,
            'username': project.username,
            'nickname': nickname  # 添加 nickname 字段
        })

    # 返回项目列表的 JSON 格式
    return jsonify(project_list)


# 获取所有用户接口，接收GET请求，要求JWT认证
@app.route('/users', methods=['GET'])
@jwt_required()  # 如果需要验证用户身份，可以添加这一行
def get_users():
    users = User.query.all()  # 查询所有用户
    return jsonify([{'id': user.id, 'username': user.username, 'nickname': user.nickname} for user in users]), 200


# 查看用户个人信息，接收GET请求
@app.route('/profile', methods=['GET'])
@jwt_required()  # 确保用户登录
def get_user_profile():
    # 获取当前登录用户信息
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()

    if user:
        # 返回用户信息（不包括密码）
        return jsonify({
            'username': user.username,
            'nickname': user.nickname,
            'gender': user.gender,
            'birthday': user.birthday,
            'signature': user.signature,
            'school': user.school,
            'major': user.major,
            'interests': user.interests
        })
    else:
        return jsonify({'error': 'User not found'}), 404
        

# 编辑用户个人信息，接收PUT请求
@app.route('/edit-profile', methods=['PUT'])
@jwt_required()  # 确保用户登录
def edit_user_profile():
    # 获取当前登录用户
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()

    if user:
        # 从请求体中获取新的用户信息
        data = request.json

        # 更新可编辑的字段，只有在提供非空值时才进行更新
        if 'nickname' in data and data['nickname'] != '':
            user.nickname = data['nickname']
        if 'gender' in data and data['gender'] != '':
            user.gender = data['gender']
        if 'birthday' in data and data['birthday'] != '':
            user.birthday = data['birthday']
        if 'signature' in data and data['signature'] != '':
            user.signature = data['signature']
        if 'school' in data and data['school'] != '':
            user.school = data['school']
        if 'major' in data and data['major'] != '':
            user.major = data['major']
        if 'interests' in data and data['interests'] != '':
            user.interests = data['interests']

        # 提交更改到数据库
        db.session.commit()

        return jsonify({'message': 'Profile updated successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404


# 主程序入口
if __name__ == '__main__':
    # 在应用程序上下文中创建数据库表
    with app.app_context():
        db.drop_all() # 删除数据库表
        db.create_all()  # 创建数据库表
    # 启动应用程序，开启调试模式
    app.run(debug=True)
