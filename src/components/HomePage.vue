<template>
  <div class="homepage-container">
    <h1 class="homepage-title">欢迎来到项目演示页面</h1>
    <div class="button-group">
      <button @click="goToRegister" class="homepage-button">注册</button>
      <button @click="goToLogin" class="homepage-button">登录</button>
      <button @click="goToCreateProject" class="homepage-button">创建项目</button>
      <button @click="goToViewProjects" class="homepage-button">查看项目</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  methods: {
    goToRegister() {
      this.$router.push('/register');
    },
    goToLogin() {
      this.$router.push('/login');
    },
    goToCreateProject() {
      this.$router.push('/create-project');
    },
    goToViewProjects() {
      this.$router.push('/projects');
    }
  }
};
</script>

<style scoped>
.homepage-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f4f6f9;
}

.homepage-title {
  font-size: 36px;
  color: #333;
  margin-bottom: 40px;
}

.button-group {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.homepage-button {
  width: 200px;
  padding: 15px;
  margin: 10px;
  font-size: 18px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.homepage-button:hover {
  background-color: #3ca772;
  transform: translateY(-2px);
}

.homepage-button:active {
  background-color: #3498db;
  transform: translateY(0);
}
</style>
