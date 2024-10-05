<template>
  <div id="app">
    <h1>Project Demo</h1>
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/register">Register</router-link> |
      <router-link to="/login">Login</router-link> |
      <router-link to="/create-project">Create Project</router-link> |
      <router-link to="/projects">View Projects</router-link> |
      <router-link to="/users">View Users</router-link> |
      <router-link :to="`/user/${username}`">My Profile</router-link> |
      <router-link to="/edit-profile">Edit Profile</router-link> |
      <button class = 'logout' @click="logout">Logout</button> <!-- 添加退出登录按钮 -->
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: ''  // 用户名初始化为空
    };
  },
  created() {
    const token = localStorage.getItem('token');

    if (token) {
      axios.get('http://localhost:5000/profile', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }).then(response => {
        this.username = response.data.username;  // 获取并设置用户名
      }).catch(error => {
        console.error('Failed to fetch user profile:', error);
      });
    } else {
      console.error('JWT Token not found. Please login.');
    }
  },
  methods: {
    logout() {
      // 清除token并重定向到登录页面
      localStorage.removeItem('token');
      this.username = ''; // 清空用户名
      this.$router.push('/login'); // 跳转到登录页
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
nav {
  margin-bottom: 20px;
}
.logout {
  cursor: pointer; /* 添加光标样式 */
  border: none; /* 去掉按钮边框 */
  background-color: transparent; /* 背景透明 */
  color: #42b983; /* 按钮字体颜色 */
  font-size: 16px; /* 字体大小 */
}
</style>
