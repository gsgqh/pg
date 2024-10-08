<template>
    <div class="messages-container">
      <h1 class="messages-title">我的消息</h1>
      <div v-if="messages.length === 0" class="no-messages">暂无消息</div>
      <div v-for="message in messages" :key="message.id" class="message-item" :class="{ read: message.is_read }">
        <div class="message-content">{{ message.content }}</div>
        <div class="message-info">
          <span class="sender">{{ message.sender }}</span>
          <span class="timestamp">{{ formatTimestamp(message.timestamp) }}</span>
          <button v-if="!message.is_read" @click="markAsRead(message.id)" class="mark-read-button">标记为已读</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
import axios from 'axios';

export default {
  name: 'MessagesPage',
  data() {
    return {
      messages: []
    };
  },
  created() {
    this.fetchMessages();
  },
  methods: {
    async fetchMessages() {
      try {
        const response = await axios.get('http://localhost:5000/messages', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}` // 使用 JWT 进行认证
          }
        });
        this.messages = response.data;
      } catch (error) {
        console.error("获取消息失败:", error);
      }
    },
    async markAsRead(messageId) {
      try {
        await axios.post(`http://localhost:5000/messages/${messageId}/read`, {}, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}` // 使用 JWT 进行认证
          }
        });
        this.fetchMessages(); // 更新消息列表
      } catch (error) {
        console.error("标记为已读失败:", error);
      }
    },
    formatTimestamp(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString(); // 格式化时间戳
    }
  }
};
  </script>
  
  <style scoped>
  .messages-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    background-color: #f4f6f9;
    min-height: 100vh;
  }
  
  .messages-title {
    font-size: 36px;
    color: #333;
    margin-bottom: 20px;
  }
  
  .no-messages {
    font-size: 18px;
    color: #666;
  }
  
  .message-item {
    background-color: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    width: 100%;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    position: relative;
  }
  
  .message-item.read {
    background-color: #f0f0f0; /* 已读消息的背景颜色 */
  }
  
  .message-content {
    font-size: 16px;
    margin-bottom: 10px;
  }
  
  .message-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .sender {
    font-weight: bold;
  }
  
  .timestamp {
    color: #999;
    font-size: 14px;
  }
  
  .mark-read-button {
    padding: 5px 10px;
    background-color: #42b983;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .mark-read-button:hover {
    background-color: #3ca772;
  }
  </style>
  