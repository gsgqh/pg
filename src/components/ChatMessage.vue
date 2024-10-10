<template>
  <!-- 背景容器 -->
  <div class="particles-background"></div>

  <!-- 聊天容器 -->
  <div id="chat">
    <h2 class="chat-header">与 {{ recipientNickname }} 聊天</h2>
    <div class="messages" ref="messages">
      <div
        v-for="(message, index) in chatHistory"
        :key="message.id"
        :class="{
          'message': true,
          'sent': message.sender_nickname === senderNickname,
          'received': message.sender_nickname !== senderNickname
        }"
      >
        <div v-if="shouldShowTimestamp(index)" class="timestamp">
          {{ formatDate(message.timestamp) }}
        </div>
        <div class="message-content">
          <p>{{ message.message }}</p>
        </div>
      </div>
    </div>
    <div class="message-input">
      <input
        v-model="newMessage"
        @keyup.enter="sendMessage"
        placeholder="输入消息..."
        class="input-field"
      />
      <button @click="sendMessage" class="send-button">发送</button>
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
      recipientId: this.$route.params.recipientId,
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
        this.scrollToBottom();
      } catch (error) {
        console.error('Error fetching chat history:', error);
      }
    },
    initializeSocket() {
      this.socket = io('http://localhost:5000');
      this.socket.on('receive_message', (data) => {
        this.chatHistory.push(data);
        this.scrollToBottom();
      });
      this.socket.on('connect_error', (error) => {
        console.error('Socket connection error:', error);
      });
    },
    sendMessage() {
      if (this.newMessage.trim() === '') return;

      const token = localStorage.getItem('token');
      const decodedToken = jwtDecode(token);
      const currentUsername = decodedToken.sub;

      const messageData = {
        message: this.newMessage,
        recipient_id: this.recipientId,
        sender_id: currentUsername
      };

      this.socket.emit('send_message', messageData, (response) => {
        if (response.success) {
          console.log('Message sent successfully');
        } else {
          console.error('Message send failed:', response.error);
        }
      });

      this.chatHistory.push({
        id: Date.now(),
        message: this.newMessage,
        sender_nickname: this.senderNickname,
        timestamp: new Date()
      });

      this.newMessage = '';
      this.scrollToBottom();
    },
    shouldShowTimestamp(index) {
      if (index === 0) return true;
      const currentMessage = this.chatHistory[index];
      const previousMessage = this.chatHistory[index - 1];
      const currentTime = new Date(currentMessage.timestamp);
      const previousTime = new Date(previousMessage.timestamp);
      const timeDifference = (currentTime - previousTime) / 60000; // 时间差（分钟）
      return timeDifference > 5;
    },
    formatDate(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const messagesDiv = this.$refs.messages;
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
      });
    }
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.disconnect();
    }
  }
};
</script>

<style scoped>
/* 粒子背景样式 */
.particles-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(-45deg, #1e3c72, #2a5298, #e8f5e9, #ffffff);
  background-size: 400% 400%;
  animation: gradientAnimation 15s ease infinite;
  z-index: -1; /* 确保背景在所有内容的后面 */
}

@keyframes gradientAnimation {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

#chat {
  max-width: 600px;
  margin: 0 auto;
  padding: 0 20px 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  height: 80vh;
  position: relative;
  z-index: 1; /* 确保聊天内容在背景之上 */
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
}

.message {
  display: flex;
  flex-direction: column;
  margin-bottom: 10px;
}

.timestamp {
  text-align: center;
  font-size: 0.75em;
  color: #888;
  margin-bottom: 5px;
}

.message-content {
  padding: 5px 6px;
  border-radius: 5px;
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

