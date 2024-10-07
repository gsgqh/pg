<template>
  <div class="register-container">
    <h2>用户注册</h2>
    <div class="input-group">
      <input v-model="username" placeholder="用户名" class="input-field" />
    </div>
    <div class="input-group">
      <input v-model="password" type="password" placeholder="密码" class="input-field" />
    </div>
    <div class="input-group">
      <input v-model="confirmPassword" type="password" placeholder="确认密码" class="input-field" />
    </div>
    <div class="input-group">
      <input v-model="nickname" placeholder="昵称" class="input-field" />
    </div>
    <button @click="register" class="register-button">注册</button>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      confirmPassword: '', // 新增确认密码字段
      nickname: '',
      errorMessage: ''
    };
  },
  methods: {
    register() {
      this.errorMessage = ''; // 清空之前的错误消息

      // 检查密码和确认密码是否一致
      if (this.password !== this.confirmPassword) {
        this.errorMessage = '密码和确认密码不一致。';
        return;
      }

      axios.post('http://localhost:5000/register', {
        username: this.username,
        password: this.password,
        nickname: this.nickname
      })
      .then(response => {
        if (response.data.success) {
          this.$router.push('/login'); // 注册成功后跳转到登录页面
        } else {
          this.errorMessage = response.data.message; // 显示服务器返回的错误消息
        }
      })
      .catch(error => {
        console.error('Error during registration:', error);
        this.errorMessage = '注册过程中发生错误。'; // 显示通用错误消息
      });
    }
  }
};
</script>

<style scoped>
.register-container {
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
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
  transition: border 0.3s ease;
}

.input-field:focus {
  border-color: #3498db;
  outline: none;
}

.register-button {
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

.register-button:hover {
  background-color: #3ca772;
}

.error-message {
  color: red;
  margin-top: 20px;
}
</style>

