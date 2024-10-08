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
    
    <!-- 注册按钮 -->
    <div class="register-link">
      <p>还没有账号？</p>
      <button @click="goToRegister" class="register-button">注册</button>
    </div>
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
    },
    goToRegister() {
      this.$router.push('/register');  // 跳转到注册页面
    }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 30px;
  background: linear-gradient(135deg, #e0f7fa, #ffffff);
  border-radius: 15px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
  font-family: 'Arial', sans-serif;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.login-container:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

h2 {
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 20px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.input-group {
  margin-bottom: 15px;
}

.input-field {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  background-color: #fafafa;
}

.input-field:focus {
  border-color: #42b983;
  box-shadow: 0 0 8px rgba(66, 185, 131, 0.3);
  outline: none;
  background-color: #ffffff;
}

.login-button {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #42b983, #3ca772);
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.2s ease, box-shadow 0.2s ease;
  font-weight: bold;
  margin-top: 10px;
}

.login-button:hover {
  background: linear-gradient(135deg, #3ca772, #3498db);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.register-link {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  font-size: 14px;
  color: #666;
}

.register-button {
  background-color: transparent;
  border: none;
  color: #3498db;
  cursor: pointer;
  text-decoration: underline;
  font-size: 14px;
  padding: 0;
  margin-left: 5px;
  transition: color 0.3s ease;
}

.register-button:hover {
  color: #2980b9;
}

.error-message {
  color: #e74c3c;
  margin-top: 15px;
  font-size: 14px;
  background: #fdecea;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>

