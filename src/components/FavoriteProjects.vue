<template>
  <div class="favorites-container">
    <h2>我的收藏项目</h2>
    <ul class="favorites-list">
      <li v-for="project in favoriteProjects" :key="project.id" class="project-card">
        <p class="project-created-by">
          <router-link :to="'/user/' + project.username" class="project-link">
            <img :src="project.creatorAvatar" alt="头像" class="creator-avatar" />
            {{ project.nickname }}
          </router-link>
        </p>
        <h3 class="project-title">{{ project.title }}</h3>
        <p class="project-content">{{ project.content }}</p>

        <div class="button-container">
          <button 
            @click="joinProject(project.id)" 
            class="join-button"
          >
            加入项目
          </button>
          <button 
            @click="toggleFavorite(project)" 
            class="favorite-button" 
            :class="{ favorited: project.isFavorited }"
          >
            取消收藏
          </button>
        </div>
        <p v-if="message" class="message">{{ message }}</p>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

export default {
  name: 'FavoriteProjects',
  data() {
    return {
      favoriteProjects: [],
      userId: null,
      message: '' // 消息状态
    };
  },
  methods: {
    fetchFavoriteProjects() {
      axios.get(`http://localhost:5000/users/${this.userId}/favorites`)
        .then(response => {
          this.favoriteProjects = response.data;
        })
        .catch(error => {
          console.error("获取收藏项目时出错: ", error);
        });
    },
    toggleFavorite(project) {
      axios.post('http://localhost:5000/projects/unfavorite', {
        user_id: this.userId,
        project_id: project.id
      })
      .then(() => {
        this.favoriteProjects = this.favoriteProjects.filter(fav => fav.id !== project.id);
      })
      .catch(error => {
        console.error("取消收藏时出错: ", error);
      });
    },
    joinProject(projectId) {
      axios.post(`http://localhost:5000/projects/${projectId}/participate`, {}, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      })
      .then(response => {
        this.message = response.data.message; // 显示成功消息
      })
      .catch(error => {
        console.error("加入项目时出错: ", error);
        this.message = error.response ? error.response.data.message : "网络错误";
      });
    }
  },
  mounted() {
    const token = localStorage.getItem('token');
    if (token) {
      const decodedToken = jwtDecode(token);
      this.userId = decodedToken.sub;
    }
    this.fetchFavoriteProjects();
  }
};
</script>

<style scoped>
.favorites-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 20px;
}

.favorites-list {
  list-style-type: none;
  padding: 0;
}

.project-card {
  background-color: #fff;
  margin-bottom: 20px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  position: relative;
}

.project-created-by {
  font-size: 14px;
  color: #7f8c8d;
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.creator-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.project-title {
  font-size: 22px;
  color: #2c3e50;
  margin: 0 0 10px;
}

.project-content {
  font-size: 16px;
  color: #34495e;
  margin-bottom: 15px;
}

.button-container {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
}

.join-button {
  padding: 8px 15px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s ease;
}

.join-button:hover {
  background-color: #3ca772;
  transform: translateY(-2px);
}

.favorite-button {
  padding: 8px 15px;
  background-color: #b2bec3;
  color: #2d3436;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s ease;
}

.favorite-button:hover {
  background-color: #636e72;
  transform: translateY(-2px);
}

.favorited {
  background-color: #d63031;
  color: #fff;
}

.message {
  margin-top: 10px;
  color: #2c3e50;
  font-weight: bold;
}
</style>
