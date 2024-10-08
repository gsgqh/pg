<template>
    <!-- 背景容器 -->
    <div class="particles-background"></div>

  <div class="register-container">
    <h2>用户注册</h2>
    <div class="input-group">
      <input v-model="username" placeholder="用户名" class="input-field" />
      <p v-if="usernameError" class="error-message">{{ usernameError }}</p>
    </div>
    <div class="input-group">
      <input v-model="password" type="password" placeholder="密码" class="input-field" />
    </div>
    <div class="input-group">
      <input v-model="confirmPassword" type="password" placeholder="确认密码" class="input-field" />
    </div>
    <div class="input-group">
      <input v-model="nickname" placeholder="昵称" class="input-field" />
      <p v-if="nicknameError" class="error-message">{{ nicknameError }}</p>
    </div>

    <!-- 头像选择 -->
    <div class="avatar-selection">
      <h3>选择头像:</h3>
      <div class="avatar-options">
        <img
          v-for="avatar in avatars"
          :key="avatar.id"
          :src="require(`@/assets/${avatar.file}`)"
          :alt="`头像 ${avatar.id}`"
          class="avatar"
          :class="{ selected: selectedAvatar === avatar.file }"
          @click="selectAvatar(avatar.file)"
        />
      </div>
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
      confirmPassword: '',
      nickname: '',
      selectedAvatar: '', // 默认未选择头像
      errorMessage: '',
      usernameError: '',
      nicknameError: '',
      maxUsernameLength: 30,
      maxNicknameLength: 20,
      avatars: [
        { id: 1, file: '1.png' },
        { id: 2, file: '2.png' },
        { id: 3, file: '3.png' },
        { id: 4, file: '4.png' },
        { id: 5, file: '5.png' },
        { id: 6, file: '6.png' },
        { id: 7, file: '7.png' },
        { id: 8, file: '8.png' },
        { id: 9, file: '9.png' },
        { id: 10, file: '10.png' }
      ],
    };
  },
  methods: {
    selectAvatar(avatar) {
      this.selectedAvatar = avatar; // 设置选中的头像
    },
    register() {
      this.errorMessage = '';
      this.usernameError = '';
      this.nicknameError = '';

      if (this.username.length > this.maxUsernameLength) {
        this.usernameError = `用户名不能超过 ${this.maxUsernameLength} 个字符。`;
        return;
      }

      if (this.nickname.length > this.maxNicknameLength) {
        this.nicknameError = `昵称不能超过 ${this.maxNicknameLength} 个字符。`;
        return;
      }

      if (this.password !== this.confirmPassword) {
        this.errorMessage = '密码和确认密码不一致。';
        return;
      }

      if (!this.selectedAvatar) {
        this.errorMessage = '请选择头像。';
        return;
      }

      axios.post('http://localhost:5000/register', {
        username: this.username,
        password: this.password,
        nickname: this.nickname,
        avatar: this.selectedAvatar, // 将选择的头像传给后端
      })
      .then(response => {
        if (response.data.success) {
          this.$router.push('/login'); // 注册成功后跳转到登录页面
        } else {
          this.errorMessage = response.data.message;
        }
      })
      .catch(error => {
        console.error('Error during registration:', error);
        this.errorMessage = '注册过程中发生错误。';
      });
    },
  },
};
</script>

<style scoped>
/* 粒子背景样式 */
.particles-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(-45deg, #1e3c72, #2a5298, #e8f5e9, #ffffff);
  background-size: 400% 400%;
  animation: gradientAnimation 15s ease infinite;
  z-index: -1; /* 确保背景在所有内容的后面 */
}

@keyframes gradientAnimation {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.register-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 30px;
  background: linear-gradient(135deg, #e0f7fa, #ffffff);
  border-radius: 15px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
  font-family: 'Arial', sans-serif;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
  z-index: 1; /* 确保内容在背景上方 */
}

.register-container:hover {
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
  width: calc(100% - 24px); /* 确保与按钮对齐 */
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  background-color: #fafafa;
  margin: 0 auto; /* 保持居中 */
}

.input-field:focus {
  border-color: #42b983;
  box-shadow: 0 0 8px rgba(66, 185, 131, 0.3);
  outline: none;
  background-color: #ffffff;
}

.avatar-selection {
  margin: 20px 0;
}

.avatar-options {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 10px;
}

.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  cursor: pointer;
  border: 3px solid transparent;
  transition: border-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.avatar:hover {
  border-color: #3498db;
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.selected {
  border-color: #42b983;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  transform: scale(1.1);
}

.register-button {
  width: calc(100% - 24px); /* 与输入框保持一致 */
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

.register-button:hover {
  background: linear-gradient(135deg, #3ca772, #3498db);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.error-message {
  color: #e74c3c;
  margin-top: 5px;
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
