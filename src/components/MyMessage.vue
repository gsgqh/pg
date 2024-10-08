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
    padding: 30px;
    background: linear-gradient(135deg, #92959b, #ffffff);
    min-height: 100vh;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
    font-family: 'Arial', sans-serif;
  }
  
  .messages-title {
    font-size: 32px;
    color: #2c3e50;
    margin-bottom: 20px;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  }
  
  .no-messages {
    font-size: 18px;
    color: #666;
    margin-top: 20px;
    text-align: center;
  }
  
  .message-item {
    background-color: #fff;
    border-radius: 12px;
    padding: 20px;
    margin: 10px 0;
    width: 100%;
    max-width: 800px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    opacity: 0;
    transform: translateY(20px);
    animation: fadeInUp 0.5s forwards;
  }
  
  .message-item:hover {
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    transform: translateY(-5px);
  }
  
  .message-item.read {
    background-color: #f0f0f0;
  }
  
  @keyframes fadeInUp {
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .message-content {
    font-size: 16px;
    margin-bottom: 10px;
    color: #34495e;
    line-height: 1.6;
  }
  
  .message-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 10px;
  }
  
  .sender {
    font-weight: bold;
    color: #3498db;
    text-shadow: 0.5px 0.5px rgba(0, 0, 0, 0.1);
  }
  
  .timestamp {
    color: #999;
    font-size: 14px;
  }
  
  .mark-read-button {
    padding: 8px 12px;
    background: linear-gradient(135deg, #42b983, #3ca772);
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.3s ease, transform 0.2s ease, box-shadow 0.2s ease;
    font-weight: bold;
  }
  
  .mark-read-button:hover {
    background: linear-gradient(135deg, #3ca772, #3498db);
    transform: translateY(-2px);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  }
  
  .mark-read-button:active {
    background: #3498db;
  }
  
  .mark-read-button:focus {
    outline: none;
  }
  
  body::-webkit-scrollbar {
    width: 0; /* 隐藏滚动条 */
  }
  </style>
  
  