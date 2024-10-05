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
      <router-link to="/edit-profile">edit Profile</router-link>
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
</style>
