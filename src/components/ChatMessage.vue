<template>
  <div id="chat">
    <h2 class="chat-header">与 {{ recipientNickname }} 聊天</h2>
    <div class="messages" ref="messages">
      <div
        v-for="message in chatHistory"
        :key="message.id"
        :class="{'message': true, 'sent': message.sender_nickname === senderNickname, 'received': message.sender_nickname !== senderNickname}">
        <div class="message-content">
          <!-- 对方的消息不显示昵称 -->
          <p>{{ message.message }}</p>
          <span class="message-timestamp">{{ formatDate(message.timestamp) }}</span>
        </div>
      </div>
    </div>
    <div class="message-input">
      <input
        v-model="newMessage"
        @keyup.enter="sendMessage"
        placeholder="Type your message..."
        class="input-field"
      />
      <button @click="sendMessage" class="send-button">Send</button>
    </div>
  </div>
</template>

<script>
import { io } from 'socket.io-client';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

export default {
  data() {
    return {
      recipientId: this.$route.params.recipientId, // 从路由获取接收者ID
      recipientNickname: '',
      senderNickname: '',
      chatHistory: [],
      newMessage: '',
      socket: null
    };
  },
  created() {
    this.fetchChatHistory();
    this.initializeSocket();
  },
  methods: {
    async fetchChatHistory() {
      const token = localStorage.getItem('token');
      try {
        const response = await axios.get(`http://localhost:5000/chat/${this.recipientId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.recipientNickname = response.data.recipient_nickname;
        this.senderNickname = response.data.sender_nickname;
        this.chatHistory = response.data.chat_history;
        this.scrollToBottom(); // 初始化时滚动到底部
      } catch (error) {
        console.error('Error fetching chat history:', error);
      }
    },
    initializeSocket() {
      this.socket = io('http://localhost:5000'); // 连接到后端 Socket.IO 服务器

      this.socket.on('receive_message', (data) => {
        this.chatHistory.push(data);
        this.scrollToBottom(); // 新消息到达后滚动到底部
      });

      this.socket.on('connect_error', (error) => {
        console.error('Socket connection error:', error);
      });
    },
    sendMessage() {
      if (this.newMessage.trim() === '') {
        return; // 防止发送空消息
      }

      const token = localStorage.getItem('token');
      const decodedToken = jwtDecode(token);
      const currentUsername = decodedToken.sub;

      const messageData = {
        message: this.newMessage,
        recipient_id: this.recipientId,
        sender_id: currentUsername
      };

      // 发送消息到后端
      this.socket.emit('send_message', messageData, (response) => {
        if (response.success) {
          console.log('Message sent successfully');
        } else {
          console.error('Message send failed:', response.error);
        }
      });

      // 直接将新消息添加到聊天记录
      this.chatHistory.push({
        id: Date.now(),
        message: this.newMessage,
        sender_nickname: this.senderNickname,
        timestamp: new Date()
      });

      // 清空输入框
      this.newMessage = '';

      // 滚动到底部以显示新发送的消息
      this.scrollToBottom();
    },
    formatDate(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString(); // 格式化时间戳
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const messagesDiv = this.$refs.messages;
        messagesDiv.scrollTop = messagesDiv.scrollHeight; // 滚动到底部
      });
    }
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.disconnect(); // 组件销毁时断开连接
    }
  }
};
</script>


<style scoped>
#chat {
  max-width: 600px;
  margin: 0 auto;
  padding: 0 20px 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #f9f9f9;
  display: flex;
  flex-direction: column;
  height: 80vh;
}

.chat-header {
  font-size: 18px;
  text-align: center;
  background-color: #42b983;
  color: #fff;
  padding: 10px;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  margin: 0;
}

.messages {
  flex: 1;
  overflow-y: auto;
  margin: 10px 0;
  padding: 10px;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.message {
  display: flex;
  margin-bottom: 10px;
}

.message-content {
  padding: 10px 15px;
  border-radius: 10px;
  background-color: #e6e6e6;
  word-wrap: break-word;
  max-width: 75%;
  width: fit-content;
}

.sent .message-content {
  background-color: #42b983;
  color: #fff;
  margin-left: auto;
  text-align: right;
}

.received .message-content {
  background-color: #f0f0f0;
  color: #333;
}

.message-timestamp {
  display: block;
  font-size: 0.8em;
  color: #999;
  margin-top: 5px;
  text-align: right;
}

.message-input {
  display: flex;
  align-items: center;
  padding: 10px;
  background-color: #fff;
  border-top: 1px solid #ddd;
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
}

.input-field {
  flex: 1;
  padding: 10px;
  margin-right: 10px;
  border: 1px solid #ddd;
  border-radius: 20px;
  font-size: 14px;
  box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.1);
}

.input-field:focus {
  border-color: #42b983;
  outline: none;
}

.send-button {
  background-color: #42b983;
  color: #fff;
  border: none;
  border-radius: 20px;
  padding: 10px 15px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.send-button:hover {
  background-color: #3ca772;
}
</style>
