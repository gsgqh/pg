<template>
    <div v-if="user" class="profile-card">
      <div class="profile-header">
        <router-link :to="`/user/${user.username}`">
          <img :src="user.avatar ? `/assets/${user.avatar}` : defaultAvatar" alt="用户头像" class="profile-avatar" />
        </router-link>
        <router-link :to="`/user/${user.username}`">
          <h2 class="profile-username">{{ user.username }}</h2>
        </router-link>
        <p class="profile-nickname">{{ user.nickname || '未提供昵称' }}</p>
      </div>
  
      <div class="actions">
        <button @click="toggleProjects">我的项目</button>
        <div v-if="showProjects">
          <button @click="goToProjectManagement">项目管理</button>
          <button @click="goToParticipatedProjects">参与的项目</button>
        </div>
  
        <button @click="goToFavorites">我的收藏</button>
        <button @click="goToMessages">我的消息{{ unreadCount > 0 ? ` (${unreadCount})` : '' }}</button>
        <button @click="goToCreateProject">创建项目</button>
      </div>
    </div>
    <p v-else>加载中...</p>
</template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        user: null,
        defaultAvatar: '/assets/default-avatar.png',
        showProjects: false,
        unreadCount: 0 // 新增属性，用于存储未读消息数
      };
    },
    created() {
      const username = this.$route.params.username;
      this.fetchUserProfile(username);
      this.fetchUnreadMessageCount(); // 请求未读消息数
    },
    methods: {
      async fetchUserProfile(username) {
        try {
  
          const response = await axios.get(`http://localhost:5000/user/${username}`, {});
  
          this.user = response.data;
        } catch (error) {
          console.error('获取用户信息失败:', error);
          alert('获取用户信息失败，请检查是否已登录');
        }
      },
      async fetchUnreadMessageCount() {
        try {
          const response = await axios.get('http://localhost:5000/unread-count', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          });
  
          this.unreadCount = response.data.unread_count; // 更新未读消息数
        } catch (error) {
          console.error('获取未读消息数失败:', error);
        }
      },
      toggleProjects() {
        this.showProjects = !this.showProjects;
      },
      goToProjectManagement() {
        this.$router.push('/projects/my-projects');
      },
      goToParticipatedProjects() {
        this.$router.push('/my-participate-projects');
      },
      goToFavorites() {
        this.$router.push('/favorites');
      },
      goToMessages() {
        this.$router.push('/messages');
      },
      goToCreateProject() {
        this.$router.push('/create-project');
      }
    }
  };
  </script>
  
  <style scoped>
  .profile-card {
    text-align: center;
    margin-top: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    padding: 20px;
  }
  
  .profile-avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
  }
  
  .profile-username {
    font-size: 24px;
    margin: 10px 0;
    color: #2c3e50;
  }
  
  .profile-nickname {
    font-size: 18px;
    color: #666;
    margin-bottom: 20px;
  }
  
  .actions {
    margin-top: 20px;
  }
  
  .actions button {
    padding: 10px 15px;
    margin: 5px;
    border: none;
    border-radius: 5px;
    background-color: #3498db;
    color: white;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .actions button:hover {
    background-color: #2980b9;
  }
  </style>
  