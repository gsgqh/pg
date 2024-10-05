<template>
    <div class="profile">
      <h2>我的信息</h2>
      <div>
        <p><strong>用户名:</strong> {{ user.username }}</p>
        <p><strong>昵称:</strong> {{ user.nickname }}</p>
        <p><strong>性别:</strong> {{ user.gender }}</p>
        <p><strong>生日:</strong> {{ user.birthday }}</p>
        <p><strong>签名:</strong> {{ user.signature }}</p>
        <p><strong>学校:</strong> {{ user.school }}</p>
        <p><strong>专业:</strong> {{ user.major }}</p>
        <p><strong>兴趣:</strong> {{ user.interests }}</p>
      </div>
      <router-link to="/edit-profile">编辑信息</router-link>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        user: {
          username: '',
          nickname: '',
          gender: '',
          birthday: '',
          signature: '',
          school: '',
          major: '',
          interests: ''
        }
      };
    },
    created() {
      this.fetchUserProfile();
    },
    methods: {
      async fetchUserProfile() {
        try {
          const response = await axios.get('http://localhost:5000/profile', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          });
          console.log('用户信息:', response.data); // 调试输出
          this.user = response.data;
        } catch (error) {
          console.error('获取用户信息失败:', error);
          alert('获取用户信息失败，请检查是否已登录');
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .user-profile {
    max-width: 600px;
    margin: auto;
  }
  </style>
  