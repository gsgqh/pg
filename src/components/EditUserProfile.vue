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
        interests: ''
      }
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
      } catch (error) {
        console.error('获取用户信息失败:', error);
      }
    },
    async updateProfile() {
      try {
        await axios.put('http://localhost:5000/edit-profile', this.user, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}` // 使用 JWT 进行认证
          }
        });
        alert('信息更新成功');
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
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
}

h2 {
  text-align: center;
  font-size: 24px;
  color: #333;
  margin-bottom: 30px;
}

.profile-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

label {
  font-size: 16px;
  margin-bottom: 5px;
  display: block;
  color: #555;
}

.input-field {
  width: 100%;
  padding: 10px;
  font-size: 14px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
  transition: border-color 0.3s ease;
}

.input-field:focus {
  border-color: #3498db;
  outline: none;
}

textarea.input-field {
  height: 80px;
}

.save-button {
  padding: 10px 15px;
  font-size: 16px;
  color: #fff;
  background-color: #42b983;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.save-button:hover {
  background-color: #3ca772;
  transform: translateY(-2px);
}

.save-button:active {
  background-color: #3498db;
  transform: translateY(0);
}
</style>
