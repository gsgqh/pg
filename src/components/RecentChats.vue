<template>
    <div class="chat-container">
      <h1>最近聊天</h1>
      <ul v-if="recentChats.length" class="chat-list">
        <li v-for="chat in recentChats" :key="chat.chat_with_id" class="chat-item" @click="startChat(chat.chat_with_id)">
          <div class="chat-header">
            <strong class="chat-username">{{ chat.chat_with }}</strong>
          </div>
          <div class="chat-message">{{ chat.message }}</div>
          <small class="chat-timestamp">{{ formatTimestamp(chat.timestamp) }}</small>
        </li>
      </ul>
      <p v-else class="no-chats">没有聊天记录。</p>
    </div>
  </template>
  
  <script>
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

export default {
  data() {
    return {
      recentChats: [],  // 存储最近聊天记录
    };
  },
  methods: {
    async fetchRecentChats() {
      try {
        const token = localStorage.getItem('token');
        const decodedToken = jwtDecode(token);
        const currentUserId = decodedToken.sub;
        const response = await axios.get(`http://localhost:5000/recent-chats?user_id=${currentUserId}`);
        this.recentChats = response.data;
      } catch (error) {
        console.error('Error fetching recent chats:', error);
      }
    },
    startChat(chatWithId) {
      // 使用对方用户ID作为路由参数跳转到聊天页面
      this.$router.push(`/chat/${chatWithId}`);
    },
    formatTimestamp(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString();
    }
  },
  created() {
    this.fetchRecentChats();
  },
};
</script>

  
  <style scoped>
  .chat-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background: linear-gradient(135deg, #e0f7fa, #ffffff);
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .chat-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
  }
  
  h1 {
    text-align: center;
    font-size: 32px;
    color: #2c3e50;
    margin-bottom: 20px;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  }
  
  .chat-list {
    list-style: none;
    padding: 0;
  }
  
  .chat-item {
    padding: 15px;
    margin: 10px 0;
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    cursor: pointer;
    transition: box-shadow 0.3s ease, transform 0.3s ease;
    display: flex;
    flex-direction: column;
  }
  
  .chat-item:hover {
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    transform: translateY(-3px);
  }
  
  .chat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .chat-username {
    font-weight: bold;
    color: #007bff;
    font-size: 18px;
    transition: color 0.3s ease;
  }
  
  .chat-username:hover {
    color: #0056b3;
  }
  
  .chat-message {
    margin: 10px 0;
    color: #333;
    font-size: 16px;
    line-height: 1.5;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
  }
  
  .chat-timestamp {
    align-self: flex-end;
    font-size: 12px;
    color: #999;
    margin-top: auto;
    background-color: #f0f0f0;
    padding: 2px 6px;
    border-radius: 5px;
  }
  
  .no-chats {
    color: #888;
    text-align: center;
    margin-top: 40px;
    font-size: 18px;
    background-color: #fafafa;
    padding: 10px;
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    transition: background-color 0.3s ease;
  }
  
  .no-chats:hover {
    background-color: #f5f5f5;
  }
  </style>
  
  