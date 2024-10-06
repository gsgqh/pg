<template>
  <div>
    <h2>Login</h2>
    <input v-model="loginUsername" placeholder="Username" />
    <input v-model="loginPassword" type="password" placeholder="Password" />
    <button @click="login">Login</button>
    <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p> <!-- 显示错误消息 -->
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      loginUsername: '',
      loginPassword: '',
      errorMessage: ''  // 用于存储错误消息
    };
  },
  methods: {
    login() {
      this.errorMessage = '';  // 清空之前的错误消息
      axios.post('http://localhost:5000/login', {
        username: this.loginUsername,
        password: this.loginPassword
      })
      .then(response => {
        if(response.data.success) {
          // 登录成功，获取访问令牌
          const accessToken = response.data.access_token;
          // 存储访问令牌
          localStorage.setItem('token', accessToken);
          // 登录成功后跳转到项目列表
          this.$router.push('/projects').then(() => {
            window.location.reload(); // 刷新页面
          });
        } else {
          this.errorMessage = response.data.message;  // 显示后端返回的消息
        }
      })
      .catch(error => {
        // 处理错误
        if (error.response) {
          // 根据后端返回的消息显示相应错误
          this.errorMessage = error.response.data.message;  // 显示后端返回的消息
        } else {
          this.errorMessage = 'An error occurred during login.';  // 通用错误消息
        }
      });
    }
  }
};
</script>
