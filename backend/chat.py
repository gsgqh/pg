from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from model import db, User, Project, ChatMessage
from flask_socketio import SocketIO
from sqlalchemy.orm import joinedload

chat = Blueprint('chat', __name__)

socketio = SocketIO(cors_allowed_origins='*')

# 发送消息接口
@chat.route('/chat/send', methods=['POST'])
@jwt_required()  # 确保用户登录
def send_message():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    # 获取消息的接收者ID和消息内容
    recipient_id = data.get('recipient_id')
    message_content = data.get('message')

    if not recipient_id or not message_content:
        return jsonify(message="Recipient ID and message cannot be empty", success=False), 400

    # 创建新消息对象
    new_message = ChatMessage(sender_id=current_user_id, recipient_id=recipient_id, message=message_content)

    # 将消息添加到数据库会话
    db.session.add(new_message)
    db.session.commit()

    return jsonify(message="Message sent", success=True), 201


# 获取用户聊天记录接口
@chat.route('/chat/<int:recipient_id>', methods=['GET'])
@jwt_required()  # 确保用户登录
def get_chat_history(recipient_id):
    current_user_id = get_jwt_identity()

     # 查询聊天记录，并预加载发送者和接收者
    messages = ChatMessage.query.options(
        joinedload(ChatMessage.sender),
        joinedload(ChatMessage.recipient)
    ).filter(
        (ChatMessage.sender_id == current_user_id) & (ChatMessage.recipient_id == recipient_id) |
        (ChatMessage.sender_id == recipient_id) & (ChatMessage.recipient_id == current_user_id)
    ).order_by(ChatMessage.timestamp).all()

    # 构建消息列表
    chat_history = []
    for message in messages:
        chat_history.append({
            'id': message.id,
            'sender_id': message.sender_id,
            'sender_nickname': message.sender.nickname,
            'recipient_id': message.recipient_id,
            'recipient_nickname': message.recipient.nickname,
            'message': message.message,
            'timestamp': message.timestamp.isoformat()
        })
    
    sender_user = User.query.get(current_user_id)
    recipient_user = User.query.get(recipient_id)
    recipient_nickname = recipient_user.nickname  # 获取接收者昵称
    sender_nickname = sender_user.nickname  # 获取发送者昵称

    return jsonify({
        'chat_history': chat_history,
        'recipient_nickname': recipient_nickname,  # 返回接收者昵称
        'sender_nickname': sender_nickname if messages else '',  # 返回发送者昵称
    }), 200

# 处理接收消息事件
@socketio.on('send_message')
def handle_send_message(data):
    
    message = data['message']
    recipient_id = data['recipient_id']
    sender_id = data['sender_id']
    print('Message sent:', message)
    # 保存消息到数据库
    new_message = ChatMessage(sender_id=sender_id, recipient_id=recipient_id, message=message)
    db.session.add(new_message)
    db.session.commit()

    # 向接收者发送消息
    socketio.emit('receive_message', {
        'message': message,
        'sender_id': sender_id,
        'recipient_id': recipient_id
    }, room=recipient_id)  # room 可以是用户ID

    # 确认消息发送成功
    return {'success': True}
    