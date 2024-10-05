<template>
    <div class="user-profile">
      <h2>编辑信息</h2>
      <form @submit.prevent="updateProfile">
        <div>
          <label for="nickname">昵称:</label>
          <input type="text" v-model="user.nickname" id="nickname" />
        </div>
        <div>
          <label for="gender">性别:</label>
          <select v-model="user.gender" id="gender">
            <option value="">请选择</option>
            <option value="男">男</option>
            <option value="女">女</option>
          </select>
        </div>
        <div>
          <label for="birthday">生日:</label>
          <input type="date" v-model="user.birthday" id="birthday" />
        </div>
        <div>
          <label for="signature">签名:</label>
          <input type="text" v-model="user.signature" id="signature" />
        </div>
        <div>
          <label for="school">学校:</label>
          <input type="text" v-model="user.school" id="school" />
        </div>
        <div>
          <label for="major">专业:</label>
          <input type="text" v-model="user.major" id="major" />
        </div>
        <div>
          <label for="interests">兴趣:</label>
          <textarea v-model="user.interests" id="interests"></textarea>
        </div>
        <button type="submit">保存</button>
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
              Authorization: `Bearer ${localStorage.getItem('token')}` // 假设使用 JWT 进行认证
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
              Authorization: `Bearer ${localStorage.getItem('token')}` // 假设使用 JWT 进行认证
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
    margin: auto;
  }
  form {
    margin-bottom: 20px;
  }
  label {
    display: block;
    margin: 10px 0 5px;
  }
  input,
  select,
  textarea {
    width: 100%;
    padding: 8px;
    margin-bottom: 10px;
  }
  button {
    padding: 10px 15px;
  }
  </style>
  