<template>
  <div>
    <h2>Users List</h2>
    <ul v-if="users.length">
      <li v-for="user in users" :key="user.id">
        <strong>Username:</strong> {{ user.username }} <br />
        <strong>Nickname:</strong> {{ user.nickname || 'No nickname provided' }}
      </li>
    </ul>
    <p v-else>No users found.</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ViewUsers',
  data() {
    return {
      users: []  // 用于存储用户数据
    };
  },
  mounted() {
    this.fetchUsers();  // 组件挂载时获取用户数据
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get('http://localhost:5000/users', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }  // 通过JWT令牌认证
        });
        this.users = response.data;  // 获取到的用户数据存储到组件的 data 中
      } catch (error) {
        console.error('Error fetching users:', error);  // 处理错误
      }
    }
  }
};
</script>

<style>
/* 添加样式用于美化显示 */
</style>
