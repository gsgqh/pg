from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
