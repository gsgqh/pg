<template>
  <div class="login-container">
    <h2>登录</h2>
    <div class="input-group">
      <input v-model="loginUsername" placeholder="用户名" class="input-field" />
    </div>
    <div class="input-group">
      <input v-model="loginPassword" type="password" placeholder="密码" class="input-field" />
    </div>
    <button @click="login" class="login-button">登录</button>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p> <!-- 显示错误消息 -->
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
          const accessToken = response.data.access_token;
          localStorage.setItem('token', accessToken);
          this.$router.push('/projects').then(() => {
            window.location.reload(); // 刷新页面
          });
        } else {
          this.errorMessage = response.data.message;  // 显示后端返回的消息
        }
      })
      .catch(error => {
        if (error.response) {
          this.errorMessage = error.response.data.message;  // 显示后端返回的消息
        } else {
          this.errorMessage = '登录过程中发生错误。';  // 通用错误消息
        }
      });
    }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
}

.input-group {
  margin-bottom: 15px;
}

.input-field {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
  transition: border-color 0.3s ease;
}

.input-field:focus {
  border-color: #3498db;
  outline: none;
}

.login-button {
  width: 100%;
  padding: 12px;
  background-color: #42b983;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #3ca772;
}

.error-message {
  color: red;
  margin-top: 15px;
  font-size: 14px;
}
</style>
