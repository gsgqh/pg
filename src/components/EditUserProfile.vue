<template>
  <!-- 背景容器 -->
  <div class="particles-background"></div>

  <div class="user-profile">
    <h2>编辑个人信息</h2>
    <form @submit.prevent="updateProfile" class="profile-form">
      <div class="form-group">
        <label for="nickname">昵称:</label>
        <input type="text" v-model="user.nickname" id="nickname" class="input-field" />
      </div>
      <div class="form-group">
        <label for="gender">性别:</label>
        <select v-model="user.gender" id="gender" class="input-field">
          <option value="">请选择</option>
          <option value="男">男</option>
          <option value="女">女</option>
        </select>
      </div>
      <div class="form-group">
        <label for="birthday">生日:</label>
        <input type="date" v-model="user.birthday" id="birthday" class="input-field" />
      </div>
      <div class="form-group">
        <label for="signature">签名:</label>
        <input type="text" v-model="user.signature" id="signature" class="input-field" />
      </div>
      <div class="form-group">
        <label for="school">学校:</label>
        <input type="text" v-model="user.school" id="school" class="input-field" />
      </div>
      <div class="form-group">
        <label for="major">专业:</label>
        <input type="text" v-model="user.major" id="major" class="input-field" />
      </div>
      <div class="form-group">
        <label for="interests">兴趣:</label>
        <textarea v-model="user.interests" id="interests" class="input-field"></textarea>
      </div>
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
      <button type="submit" class="save-button">保存</button>
    </form>

    <!-- 美化的弹窗 -->
    <div v-if="showMessage" class="custom-alert">
      <p>{{ successMessage }}</p>
    </div>
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
        interests: '',
        avatar: ''
      },
      selectedAvatar: '',
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
      showMessage: false,
      successMessage: ''
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
        this.user = response.data;
        this.selectedAvatar = this.user.avatar;
      } catch (error) {
        console.error('获取用户信息失败:', error);
      }
    },
    selectAvatar(avatar) {
      this.selectedAvatar = avatar;
      this.user.avatar = avatar;
    },
    async updateProfile() {
      try {
        const response = await axios.put('http://localhost:5000/edit-profile', this.user, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.successMessage = response.data.message;
        this.showMessage = true;

        // 3 秒后自动跳转到用户的 "我的资料" 页面
        setTimeout(() => {
          this.showMessage = false;
          this.$router.push(`/user/${this.user.username}`);
        }, 3000);
      } catch (error) {
        console.error('更新用户信息失败:', error);
        this.successMessage = '更新信息失败';
        this.showMessage = true;
      }
    }
  }
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

.user-profile {
  max-width: 500px;
  margin: 50px auto;
  padding: 30px;
  background: linear-gradient(135deg, #e0f7fa, #ffffff);
  border-radius: 15px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
  z-index: 1; /* 确保内容在背景上方 */
}

.user-profile:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

h2 {
  text-align: center;
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 20px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  align-items: center;
}

.form-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  width: 100%;
}

label {
  font-size: 16px;
  color: #555;
  font-weight: bold;
}

.input-field {
  width: 80%;
  max-width: 400px;
  padding: 10px;
  font-size: 14px;
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

textarea.input-field {
  height: 100px;
}

.save-button {
  width: 80%;
  max-width: 400px;
  padding: 12px;
  font-size: 16px;
  font-weight: bold;
  color: #fff;
  background: linear-gradient(135deg, #42b983, #3ca772);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
}

.save-button:hover {
  background: linear-gradient(135deg, #3ca772, #3498db);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.avatar-selection {
  margin: 20px 0;
}

.avatar-options {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
}

.avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.avatar:hover {
  border-color: #3498db;
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.avatar.selected {
  border-color: #42b983;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  transform: scale(1.1);
}

.custom-alert {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: #42b983;
  color: white;
  padding: 15px 30px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  font-size: 16px;
  animation: fadeInOut 3s ease-in-out;
}

@keyframes fadeInOut {
  0%, 100% { opacity: 0; }
  10%, 90% { opacity: 1; }
}
</style>

