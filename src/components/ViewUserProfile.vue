<template>
    <div class="profile">
      <h2>用户信息</h2>
      <div v-if="user">
        <p><strong>用户名:</strong> {{ user.username }}</p>
        <p><strong>昵称:</strong> {{ user.nickname }}</p>
        <p><strong>性别:</strong> {{ user.gender }}</p>
        <p><strong>生日:</strong> {{ user.birthday }}</p>
        <p><strong>签名:</strong> {{ user.signature }}</p>
        <p><strong>学校:</strong> {{ user.school }}</p>
        <p><strong>专业:</strong> {{ user.major }}</p>
        <p><strong>兴趣:</strong> {{ user.interests }}</p>
      </div>
      <!-- 只有当当前用户查看自己的信息时才显示编辑按钮 -->
      <router-link v-if="isCurrentUser" to="/edit-profile">编辑信息</router-link>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { jwtDecode } from "jwt-decode";
  
  export default {
    data() {
      return {
        user: null,  // 保存用户信息
        isCurrentUser: false  // 标记是否为当前登录用户
      };
    },
    created() {
      // 在组件创建时获取当前查看的用户名，并获取该用户的资料
      const username = this.$route.params.username;  // 从路由参数中获取要查看的用户名
      this.fetchUserProfile(username);  // 传递用户名
    },
    methods: {
      async fetchUserProfile(username) {
        try {
          const token = localStorage.getItem('token');
          const decodedToken = jwtDecode(token);  // 解码JWT令牌，获取当前用户的身份信息
          const currentUsername = decodedToken.sub;  // 获取当前登录用户的用户名
          
          // 根据传入的用户名，动态请求用户信息
          const response = await axios.get(`http://localhost:5000/user/${username}`, {
            headers: {
              Authorization: `Bearer ${token}`  // 附带JWT令牌进行认证
            }
          });
  
          console.log('用户信息:', response.data); // 调试输出
          this.user = response.data;
  
          // 比较当前登录用户和查看的用户是否一致
          this.isCurrentUser = this.user.id === currentUsername;
          console.log('当前用户:', currentUsername);
          console.log('请求的用户:', this.user.id);
          console.log('isCurrentUser:', this.isCurrentUser);
        } catch (error) {
          console.error('获取用户信息失败:', error);
          alert('获取用户信息失败，请检查是否已登录');
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .profile {
    max-width: 600px;
    margin: auto;
  }
  </style>
  