<template>
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
        <!-- 如果消息与上一条消息的时间差超过5分钟，则显示时间戳 -->
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
