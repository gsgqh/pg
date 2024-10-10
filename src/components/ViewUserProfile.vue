<template>
    <!-- 背景容器 -->
    <div class="particles-background"></div>

  <div v-if="user" class="profile-card">
    <div class="profile-header">
      <!-- 显示用户头像，如果没有头像则显示默认头像 -->
      <img :src="user.avatar ? require(`@/assets/${user.avatar}`) : defaultAvatar" alt="用户头像" class="profile-avatar" />
      <h2 class="profile-username">{{ user.username }}</h2>
    </div>
    <div class="profile-info">
      <p><strong>昵称:</strong> {{ user.nickname || '未提供昵称' }}</p>
      <p><strong>性别:</strong> {{ user.gender || '未提供性别' }}</p>
      <p><strong>生日:</strong> {{ user.birthday || '未提供生日' }}</p>
      <p><strong>签名:</strong> {{ user.signature || '未提供签名' }}</p>
      <p><strong>学校:</strong> {{ user.school || '未提供学校信息' }}</p>
      <p><strong>专业:</strong> {{ user.major || '未提供专业信息' }}</p>
      <p><strong>兴趣:</strong> {{ user.interests || '未提供兴趣' }}</p>
    </div>
    <div class="profile-actions">
      <!-- 编辑信息按钮保留在这里 -->
      <router-link v-if="isCurrentUser" to="/edit-profile" class="btn-edit">编辑信息</router-link>
    </div>
    <!-- 聊天按钮单独放置在信息卡片底部 -->
    <div v-if="!isCurrentUser" class="chat-action">
      <button @click="startChat" class="btn-chat">聊天</button>
    </div>
  </div>
  <p v-else>加载中...</p> <!-- 在 user 数据为 null 时显示加载信息 -->
</template>

<script>
// 正确导入 jwt-decode 库
import { jwtDecode } from 'jwt-decode';  // 使用命名导出方式
import axios from 'axios';

export default {
  data() {
    return {
      user: null,  // 用户信息，初始值为 null
      isCurrentUser: false,  // 标志是否是当前登录用户
      defaultAvatar: '/assets/default-avatar.png'  // 默认头像路径
    };
  },
  created() {
    const username = this.$route.params.username;  // 从路由获取当前查看的用户名
    this.fetchUserProfile(username);  // 调用方法获取用户信息
  },
  methods: {
    async fetchUserProfile(username) {
      try {
        const token = localStorage.getItem('token');
        const decodedToken = jwtDecode(token);  // 使用 jwtDecode 解码 JWT
        const currentUsername = decodedToken.sub;  // 从 JWT 中获取当前登录用户的用户名
        
        // 请求后端获取用户信息
        const response = await axios.get(`http://localhost:5000/user/${username}`, {
          headers: {
            Authorization: `Bearer ${token}`  // 附带JWT令牌进行认证
          }
        });

        this.user = response.data;  // 成功获取后设置用户信息
        this.isCurrentUser = this.user.id === currentUsername;  // 判断是否为当前登录用户
      } catch (error) {
        console.error('获取用户信息失败:', error);
        alert('获取用户信息失败，请检查是否已登录');
      }
    },
    startChat() {
      // 跳转到聊天页面，使用用户ID作为路由参数
      this.$router.push(`/chat/${this.user.id}`);
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

.create-project-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 30px;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
  position: relative;
  z-index: 1; /* 确保内容在背景上方 */
}

.profile-card {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1; /* 确保内容在背景上方 */
}
.profile-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}
.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-right: 20px;
  object-fit: cover;
}
.profile-username {
  font-size: 24px;
  font-weight: bold;
  color: #2c3e50;
}
.profile-info p {
  margin: 5px 0;
}
.profile-actions {
  margin-top: 20px;
  text-align: center;
}
.chat-action {
  margin-top: 20px;
  text-align: center;
}
.btn-edit, .btn-chat {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}
.btn-edit {
  background-color: #42b983;
  color: #fff;
  margin-right: 10px;
}
.btn-chat {
  background-color: #3498db;
  color: #fff;
}
.btn-edit:hover, .btn-chat:hover {
  opacity: 0.8;
}
</style>
