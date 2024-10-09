<template>
  <div id="app">
    <header>
      <h1>PG</h1>
      <nav>
        <!-- 仅在已登录时显示其他导航项 -->
        <router-link v-if="isLoggedIn" to="/">主页</router-link>
        <router-link v-if="isLoggedIn" to="/create-project">创建项目</router-link>
        <router-link v-if="isLoggedIn" to="/projects">查看项目</router-link>
        <router-link v-if="isLoggedIn" :to="`/user/${username}`">我的资料</router-link>
        <router-link v-if="isLoggedIn" to="/recent-chats">聊天</router-link>
        <router-link v-if="isLoggedIn" :to="`/my-page/${username}`" class="favorites-link">我的</router-link>
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
  padding: 15px 0; /* 上下内边距，不包括左右 */
  position: fixed;
  top: 0;
  left: 0; /* 确保从屏幕最左侧开始 */
  width: 100vw; /* 让导航栏宽度占据整个屏幕 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: space-between; /* 将内容两端对齐 */
  flex-wrap: wrap; /* 内容太多时换行 */
}

header h1 {
  color: #fff;
  margin: 0 20px; /* 使标题与边距之间有些空隙 */
  font-size: 24px;
}

nav {
  display: flex;
  flex-wrap: wrap; /* 允许导航项换行 */
  gap: 15px;
  margin-right: 20px; /* 使导航项与右侧有些空隙 */
  overflow-x: auto; /* 内容太多时允许水平滚动 */
  animation: slideIn 0.8s ease-in-out; /* 添加动态效果 */
}

@keyframes slideIn {
  0% {
    transform: translateX(100%);
    opacity: 0;
  }
  100% {
    transform: translateX(0);
    opacity: 1;
  }
}

nav a {
  color: #fff;
  text-decoration: none;
  padding: 5px 10px;
  font-size: 16px;
  transition: color 0.3s ease, transform 0.3s ease;
}

nav a:hover {
  color: #c9f1db;
  transform: scale(1.1);
}

.logout {
  background-color: transparent;
  color: #fff;
  border: none;
  font-size: 16px;
  cursor: pointer;
  padding: 5px 10px;
  transition: color 0.3s ease, transform 0.3s ease;
}

.logout:hover {
  color: #c9f1db;
  transform: scale(1.1);
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
    flex-direction: column;
    text-align: left;
    margin-right: 0; /* 移除右侧空隙 */
  }

  nav a, .logout {
    margin: 5px 0;
    font-size: 14px;
  }

  header h1 {
    margin-bottom: 10px;
    text-align: center;
    width: 100%;
  }
}
</style>