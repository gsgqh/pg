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
  import {jwtDecode} from 'jwt-decode'; 
  
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
        return new Date(timestamp).toLocaleString();
      }
    },
    created() {
      this.fetchRecentChats();
    },
  };
  </script>
  
  <style scoped>
  .chat-container {
    padding: 20px;
    background-color: #f8f9fa;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .chat-list {
    list-style-type: none;
    padding: 0;
  }
  
  .chat-item {
    padding: 10px;
    border-bottom: 1px solid #e0e0e0;
    cursor: pointer;
  }
  
  .chat-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .chat-username {
    font-weight: bold;
    color: #007bff;
  }
  
  .chat-message {
    margin: 5px 0;
    color: #333;
  }
  
  .chat-timestamp {
    font-size: 12px;
    color: #999;
  }
  
  .no-chats {
    color: #999;
    text-align: center;
    margin-top: 20px;
  }
  </style>
  