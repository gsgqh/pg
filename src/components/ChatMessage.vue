<template>
  <div id="chat">
    <h2>Chat with {{ recipientNickname }}</h2>
    <div class="messages" ref="messages">
      <div v-for="message in chatHistory" :key="message.id" class="message">
        <strong>{{ message.sender_nickname }}:</strong> {{ message.message }} <span>{{ formatDate(message.timestamp) }}</span>
      </div>
    </div>
    <input v-model="newMessage" @keyup.enter="sendMessage" placeholder="Type your message..." />
    <button @click="sendMessage">Send</button>
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
      senderNickname:'',
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
        this.recipientNickname = response.data.recipient_nickname; // 更新为 response.data
        this.senderNickname = response.data.sender_nickname; // 更新为 response.data
        this.chatHistory = response.data.chat_history; // 更新为 response.data
        this.scrollToBottom(); // 初始化时滚动到底部
      } catch (error) {
        console.error('Error fetching chat history:', error);
      }
    },
    initializeSocket() {
      this.socket = io('http://localhost:5000'); // 连接到后端 Socket.IO 服务器

      this.socket.on('receive_message', (data) => {
        this.chatHistory.push(data); // 将接收到的消息添加到聊天记录
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

      // 从本地存储获取 token
      const token = localStorage.getItem('token');
      const decodedToken = jwtDecode(token); // 解码JWT令牌
      const currentUsername = decodedToken.sub; // 假设用户名存储在 sub 字段
      
      const messageData = {
        message: this.newMessage,
        recipient_id: this.recipientId,
        sender_id: currentUsername // 从解码的 token 中获取当前用户的用户名
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
        id: Date.now(), // 生成一个简单的唯一 ID
        message: this.newMessage,
        sender_nickname: this.senderNickname,
        timestamp: new Date() // 设置当前时间戳
      });

      // 清空输入框
      this.newMessage = '';
      // 判断 chatHistory 长度，如果为 1 则刷新
      if (this.chatHistory.length === 1) {
        window.location.reload();
      }
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
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #f9f9f9;
}

.messages {
  height: 400px;
  overflow-y: auto;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  padding: 10px;
  background-color: #fff;
}

.message {
  margin: 5px 0;
}
</style>
