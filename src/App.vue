<template>
  <div id="app">
    <header>
      <h1>项目演示</h1>
      <nav>
        <!-- 仅在未登录时显示 注册 和 登录 -->
        <router-link v-if="!isLoggedIn" to="/register">注册</router-link>
        <router-link v-if="!isLoggedIn" to="/login">登录</router-link>

        <!-- 仅在已登录时显示其他导航项 -->
        <router-link v-if="isLoggedIn" to="/">主页</router-link>
        <router-link v-if="isLoggedIn" to="/create-project">创建项目</router-link>
        <router-link v-if="isLoggedIn" to="/projects">查看项目</router-link>
        <router-link v-if="isLoggedIn" to="/users">查看用户</router-link>
        <router-link v-if="isLoggedIn" :to="`/user/${username}`">我的资料</router-link>
        <router-link v-if="isLoggedIn" to="/edit-profile">编辑资料</router-link>
        <router-link v-if="isLoggedIn" to="/recent-chats">聊天</router-link>
        <router-link v-if="isLoggedIn" to="/favorites" class="favorites-link">我的收藏</router-link>
        <button v-if="isLoggedIn" class="logout" @click="logout">退出登录</button>
      </nav>
    </header>
    <main>
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '', // 用户名初始化为空
      isLoggedIn: false // 登录状态
    };
  },
  created() {
    const token = localStorage.getItem('token');
    if (token) {
      axios.get('http://localhost:5000/profile', {
        headers: {
          Authorization: `Bearer ${token}`
        }
      })
      .then(response => {
        this.username = response.data.username; // 获取并设置用户名
        this.isLoggedIn = true; // 设置为已登录状态
      })
      .catch(error => {
        console.error('获取用户资料失败:', error);
        this.handleAuthError();
      });
    } else {
      console.error('JWT Token 不存在，请先登录。');
      this.isLoggedIn = false;
      this.$router.push('/login'); // 未找到 Token 时自动重定向到登录页
    }
  },
  methods: {
    handleAuthError() {
      localStorage.removeItem('token'); // 清除无效的 Token
      this.isLoggedIn = false; // 设置为未登录状态
      this.$router.push('/login'); // 重定向到登录页面
    },
    logout() {
      localStorage.removeItem('token');
      this.username = ''; // 清空用户名
      this.isLoggedIn = false; // 设置为未登录状态
      this.$router.push('/login'); // 跳转到登录页
    }
  }
};
</script>

<style scoped>
/* 基本布局 */
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

/* 导航栏样式 */
header {
  background-color: #42b983;
  padding: 15px;
  position: fixed;
  top: 0;
  width: 100%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

header h1 {
  color: #fff;
  margin: 0;
  display: inline-block;
  font-size: 24px;
}

nav {
  display: inline-block;
  float: right;
}

nav a {
  color: #fff;
  text-decoration: none;
  margin: 0 10px;
  font-size: 16px;
  transition: color 0.3s ease;
}

nav a:hover {
  color: #c9f1db;
}

.logout {
  background-color: transparent;
  color: #fff;
  border: none;
  font-size: 16px;
  cursor: pointer;
  margin-left: 10px;
  transition: color 0.3s ease;
}

.logout:hover {
  color: #c9f1db;
}

/* 主体内容 */
main {
  margin-top: 100px;
  padding: 20px;
  text-align: center;
}

/* 响应式样式 */
@media (max-width: 768px) {
  nav {
    display: block;
    text-align: center;
  }

  nav a, .logout {
    display: block;
    margin: 10px 0;
  }

  header h1 {
    display: block;
    text-align: center;
    margin-bottom: 10px;
  }
}
</style>
