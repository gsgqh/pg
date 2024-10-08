from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# 定义用户模型，继承自SQLAlchemy的Model类
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)  # 用户ID，主键
    username = db.Column(db.String(80), unique=True, nullable=False)  # 用户名，唯一且不能为空
    password = db.Column(db.String(200), nullable=False)  # 密码，不能为空
    nickname = db.Column(db.String(100), nullable=False)  # 用户昵称
    gender = db.Column(db.String(10))  # 性别，值可以是 'male', 'female' 等
    birthday = db.Column(db.Date)  # 生日，使用日期类型
    signature = db.Column(db.String(200))  # 签名
    school = db.Column(db.String(200))  # 学校名称
    major = db.Column(db.String(100))  # 专业
    interests = db.Column(db.Text)  # 兴趣，文本类型，可以存储多个兴趣

# 定义项目模型，继承自SQLAlchemy的Model类
class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)  # 项目ID，主键
    title = db.Column(db.String(200), nullable=False)  # 项目标题，不能为空
    content = db.Column(db.Text, nullable=False)  # 项目内容，不能为空
    username = db.Column(db.String(80), nullable=False)  # 当前创建项目的用户的用户名，不能为空
    major_type = db.Column(db.String(20))  # 专业类型
    category = db.Column(db.String(10))  # 项目类别

    @staticmethod
    def search(keyword):
        # 使用 SQLAlchemy 进行模糊查询
        return Project.query.filter(
            (Project.title.ilike(f'%{keyword}%')) | 
            (Project.content.ilike(f'%{keyword}%'))
        ).all()
    
    def participate(self, user_id):
        # 检查用户是否已参与项目
        existing_participation = Participation.query.filter_by(
            project_id=self.id,
            user_id=user_id
        ).first()

        if existing_participation:
            return "您已申请参与该项目，状态为: " + existing_participation.status

        # 创建新的参与记录
        new_participation = Participation(
            user_id=user_id,
            project_id=self.id,
            status=ParticipationStatus.PENDING  # 初始状态为待审核
        )
        db.session.add(new_participation)
        db.session.commit()
        return "参与申请已提交，等待审核。"

    @staticmethod
    def review_participation(participation_id, action):
        participation = Participation.query.filter_by(id=participation_id).first()
        if not participation:
            return "未找到该参与申请。"
        
        if action == 'approve':
            participation.status = ParticipationStatus.PARTICIPATED
            message = "申请已通过。"
        elif action == 'reject':
            db.session.delete(participation)  # 删除该参与记录
            participation.status = ParticipationStatus.NOT_PARTICIPATED
            message = "申请已拒绝。"
        else:
            return "无效的操作。"
        
        db.session.commit()
        return message

# 定义会话模型，继承自SQLAlchemy的Model类
class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message = Column(String(500), nullable=False)
    timestamp = Column(db.DateTime, default=datetime.now)

    sender = relationship('User', foreign_keys=[sender_id])
    recipient = relationship('User', foreign_keys=[recipient_id])

# 定义收藏模型，继承自SQLAlchemy的Model类
class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 关联用户
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)  # 关联项目

    user = db.relationship('User', backref='favorites')
    project = db.relationship('Project', backref='favorites')

# 定义参与模型，继承自SQLAlchemy的Model类
class Participation(db.Model):
    __tablename__ = 'participations'

    id = db.Column(db.Integer, primary_key=True)  # 参与记录的ID，主键
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 外键，指向用户ID
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)  # 外键，指向项目ID
    status = db.Column(db.String(20), nullable=False, default='未参与')  # 参与状态，默认是未参与

    user = db.relationship('User', backref='participations')  # 用户与参与记录的一对多关系
    project = db.relationship('Project', backref='participations')  # 项目与参与记录的一对多关系

# 定义参与状态常量
class ParticipationStatus:
    NOT_PARTICIPATED = '未参与'
    PENDING = '待审核'  
    PARTICIPATED = '已参与' 

# 定义消息模型，继承自SQLAlchemy的Model类
class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)  # 消息ID，主键
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 发送者ID
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 接收者ID
    content = db.Column(db.String(200), nullable=False)  # 消息内容
    is_read = db.Column(db.Boolean, default=False)  # 已读状态，默认为未读
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())  # 时间戳

    sender = db.relationship('User', foreign_keys=[sender_id])  # 发送者
    recipient = db.relationship('User', foreign_keys=[recipient_id])  # 接收者