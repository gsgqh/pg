<template>
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
      <!-- 头像选择 -->
      <div class="avatar-selection">
        <h3>选择头像:</h3>
        <div class="avatar-options">
          <img
            v-for="avatar in avatars"
            :key="avatar.id"
            :src="`/assets/${avatar.file}`"
            :alt="`头像 ${avatar.id}`"
            class="avatar"
            :class="{ selected: selectedAvatar === avatar.file }"
            @click="selectAvatar(avatar.file)"
          />
        </div>
      </div>
      <button type="submit" class="save-button">保存</button>
    </form>
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
        avatar: ''  // 添加 avatar 字段
      },
      selectedAvatar: '', // 默认未选择头像
      avatars: [
        { id: 1, file: '1.png' },
        { id: 2, file: '2.png' },
        { id: 3, file: '3.png' },
        { id: 4, file: '4.png' },
      ],
    };
  },
  created() {
    this.fetchUserProfile();
  },
  methods: {
    async fetchUserProfile() {
      try {
        const response = await axios.get('http://localhost:5000/edit-profile', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}` // 使用 JWT 进行认证
          }
        });
        this.user = response.data;
        this.selectedAvatar = this.user.avatar; // 设定已选头像
      } catch (error) {
        console.error('获取用户信息失败:', error);
      }
    },
    selectAvatar(avatar) {
      this.selectedAvatar = avatar; // 设置选中的头像
      this.user.avatar = avatar; // 更新用户头像
    },
    async updateProfile() {
      try {
        const response = await axios.put('http://localhost:5000/edit-profile', this.user, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}` // 使用 JWT 进行认证
          }
        });
        alert(response.data.message);
      } catch (error) {
        console.error('更新用户信息失败:', error);
        alert('更新信息失败');
      }
    }
  }
};
</script>

<style scoped>
.user-profile {
  max-width: 600px;
  margin: 50px auto;
  padding: 30px;
  background: linear-gradient(135deg, #e0f7fa, #ffffff);
  border-radius: 15px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.user-profile:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

h2 {
  text-align: center;
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 30px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

label {
  font-size: 16px;
  color: #555;
  font-weight: bold;
}

.input-field {
  width: 100%;
  padding: 12px;
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
  height: 120px;
}

.save-button {
  padding: 12px 20px;
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

.save-button:active {
  background-color: #3498db;
  transform: translateY(0);
}

.save-button:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.avatar-selection {
  margin: 20px 0;
}

.avatar-options {
  display: flex;
  justify-content: space-around;
  margin-bottom: 10px;
}

.avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  cursor: pointer;
  border: 2px solid transparent;
  transition: border 0.3s ease;
}

.avatar:hover {
  border-color: #3498db;
}

.avatar.selected {
  border-color: #42b983; /* 选中后边框颜色 */
  border-width: 2px; /* 边框宽度 */
}
</style>

