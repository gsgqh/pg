<template>
  <div>
    <h2>Register</h2>
    <input v-model="username" placeholder="Username" />
    <input v-model="password" type="password" placeholder="Password" />
    <input v-model="nickname" placeholder="Nickname" /> <!-- 新增昵称输入框 -->
    <button @click="register">Register</button>
    <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p> <!-- 显示错误消息 -->
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      nickname: '',  // 用于存储昵称
      errorMessage: ''  // 用于存储错误消息
    };
  },
  methods: {
    register() {
      this.errorMessage = '';  // 清空之前的错误消息
      axios.post('http://localhost:5000/register', {
        username: this.username,
        password: this.password,
        nickname: this.nickname  // 传递昵称到后端
      })
      .then(response => {
        if (response.data.success) {
          this.$router.push('/login');  // 注册成功后跳转到登录页面
        } else {
          this.errorMessage = response.data.message;  // 设置错误消息
        }
      })
      .catch(error => {
        console.error('Error during registration:', error);
        this.errorMessage = 'An error occurred during registration.';  // 设置通用错误消息
      });
    }
  }
};
</script>
