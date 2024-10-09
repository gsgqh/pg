<template>
  <div class="profile-card" v-if="user">
    <div class="profile-header">
      <router-link :to="`/user/${user.username}`">
        <img :src="user.avatar ? `/assets/${user.avatar}` : defaultAvatar" alt="用户头像" class="profile-avatar" />
      </router-link>
      <router-link :to="`/user/${user.username}`">
        <h2 class="profile-username">用户名: {{ user.username }}</h2>
      </router-link>
      <p class="profile-nickname">昵称: {{ user.nickname || '未提供昵称' }}</p>
    </div>

    <div class="actions">
      <button @click="toggleProjects">项目管理</button>
      <div v-if="showProjects" class="project-buttons">
        <div class="project-button-wrapper">
          <button @click="goToProjectManagement" class="sub-action-button">创建的项目</button>
          <button @click="goToParticipatedProjects" class="sub-action-button">参与的项目</button>
        </div>
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
      unreadCount: 0,
    };
  },
  created() {
    const username = this.$route.params.username;
    this.fetchUserProfile(username);
    this.fetchUnreadMessageCount();
  },
  methods: {
    async fetchUserProfile(username) {
      try {
        const response = await axios.get(`http://localhost:5000/user/${username}`);
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
        this.unreadCount = response.data.unread_count;
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
  background: linear-gradient(135deg, #e0f7fa, #ffffff);
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.profile-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.profile-avatar:hover {
  transform: scale(1.05);
}

.profile-username {
  font-size: 18px;
  margin: 8px 0 4px;
  color: #2c3e50;
  font-weight: bold;
}

.profile-nickname {
  font-size: 16px;
  color: #666;
  margin-bottom: 15px;
}

.actions {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.actions button {
  padding: 14px 24px;
  width: 60%;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, #42b983, #3ca772);
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s ease, box-shadow 0.2s ease;
}

.actions button:hover {
  background: linear-gradient(135deg, #3ca772, #3498db);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.project-buttons {
  margin-top: 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  width: 100%;
}

.project-button-wrapper {
  display: flex;
  gap: 20px;
}

.sub-action-button {
  padding: 12px 28px;
  width: auto;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: #fff;
  font-size: 15px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s ease, box-shadow 0.2s ease;
}

.sub-action-button:hover {
  background: linear-gradient(135deg, #2980b9, #1f6391);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
</style>