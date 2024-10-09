<template>
  <div v-if="showWelcome" class="welcome-container">
    <div class="welcome-content">
      <h1 class="welcome-title">欢迎来到PG</h1>
      <button @click="skipWelcome" class="welcome-button">点击继续</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showWelcome: true
    };
  },
  mounted() {
    // 3秒后自动隐藏欢迎界面并导航到登录界面
    setTimeout(() => {
      this.skipWelcome();
    }, 3000);
  },
  methods: {
    skipWelcome() {
      this.showWelcome = false;
      // 导航到登录页面
      this.$router.push('/login');
    }
  }
};

</script>

<style scoped>
.welcome-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: linear-gradient(45deg, #42a5f5, #7e57c2, #42b983);
  background-size: 300% 300%;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: backgroundAnimation 6s ease infinite;
  z-index: 9999;
}

@keyframes backgroundAnimation {
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

.welcome-content {
  text-align: center;
  color: white;
  animation: fadeIn 1s ease;
  backdrop-filter: blur(5px);
  background: rgba(255, 255, 255, 0.1);
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.8);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.welcome-title {
  font-size: 32px;
  margin-bottom: 20px;
  text-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
}

.welcome-button {
  background: rgba(255, 255, 255, 0.2);
  color: #fff;
  padding: 10px 20px;
  border: 2px solid white;
  border-radius: 30px;
  cursor: pointer;
  font-size: 18px;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.welcome-button:hover {
  background-color: rgba(255, 255, 255, 0.4);
  transform: scale(1.1);
}

.welcome-button:active {
  transform: scale(1);
  background-color: rgba(255, 255, 255, 0.6);
}
</style>
