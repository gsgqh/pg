<template>
  <div v-if="user" class="profile-card">
    <div class="profile-header">
      <!-- 显示用户头像，如果没有头像则显示默认头像 -->
      <img :src="user.avatar || defaultAvatar" alt="用户头像" class="profile-avatar" />
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
      <!-- 如果是当前用户，则显示“编辑信息”按钮 -->
      <router-link v-if="isCurrentUser" to="/edit-profile" class="btn-edit">编辑信息</router-link>
      <!-- 否则显示“聊天”按钮 -->
      <button v-else @click="startChat" class="btn-chat">聊天</button>
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
      defaultAvatar: 'default-avatar.png'  // 默认头像路径
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
        this.isCurrentUser = this.user.username === currentUsername;  // 判断是否为当前登录用户
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
.profile-card {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
