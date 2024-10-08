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

</style>

