<template>
  <div>
    <h2>用户列表</h2>
    <p v-if="loading">加载中...</p> <!-- 加载状态提示 -->
    <ul v-if="users.length && !loading">
      <li v-for="user in users" :key="user.id">
        <strong>用户名:</strong> {{ user.username }} <br />
        <strong>昵称:</strong> {{ user.nickname || '未提供昵称' }}
      </li>
    </ul>
    <p v-else-if="!loading && !error">未找到用户。</p> <!-- 没有用户时显示 -->
    <p v-if="error">加载用户时出错: {{ error }}</p> <!-- 错误提示 -->
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ViewUsers',
  data() {
    return {
      users: [], // 用于存储用户数据
      loading: true, // 加载状态
      error: '' // 错误信息
    };
  },
  mounted() {
    this.fetchUsers(); // 组件挂载时获取用户数据
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get('http://localhost:5000/users', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } // 通过JWT令牌认证
        });
        this.users = response.data; // 获取到的用户数据存储到组件的 data 中
      } catch (error) {
        this.error = '获取用户数据失败'; // 捕获错误并显示
        console.error('Error fetching users:', error); // 控制台打印错误
      } finally {
        this.loading = false; // 无论请求成功与否，加载完成后都关闭加载状态
      }
    }
  }
};
</script>

<style>
/* 添加一些样式美化用户列表 */
ul {
  list-style-type: none; /* 移除默认的列表样式 */
  padding: 0;
}
li {
  background-color: #f9f9f9;
  margin: 10px 0;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
strong {
  color: #42b983;
}
</style>
