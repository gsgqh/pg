<template>
  <div class="favorites-container">
    <h2>我的收藏项目</h2>
    <ul class="favorites-list">
      <li v-for="project in favoriteProjects" :key="project.id" class="project-card">
        <div class="project-created-by">
          <router-link :to="'/user/' + project.username" class="project-link">
            <img :src="project.avatar ? `/assets/${project.avatar}` : 'default-avatar.png'" alt="创建者头像" class="creator-avatar" />
            <span>{{ project.nickname }}</span>
          </router-link>
        </div>
        <h3 class="project-title">{{ project.title }}</h3>
        <p class="project-content">{{ project.content }}</p>

        <div class="images-container">
          <img v-for="(image, index) in project.images" :key="index" :src="`${image}`" alt="项目图片" class="project-image" />
        </div>

        <div class="button-container">
          <button 
            @click="joinProject(project)" 
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
        <p v-if="project.message" class="message">{{ project.message }}</p>
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
      userId: null
    };
  },
  methods: {
    fetchFavoriteProjects() {
      axios.get(`http://localhost:5000/users/${this.userId}/favorites`)
        .then(response => {
          // 初始化项目数据时，将每个项目的 message 属性设置为空
          this.favoriteProjects = response.data.map(project => ({
            ...project,
            message: '' // 每个项目独立的消息
          }));
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
        // 过滤掉已取消收藏的项目
        this.favoriteProjects = this.favoriteProjects.filter(fav => fav.id !== project.id);
      })
      .catch(error => {
        console.error("取消收藏时出错: ", error);
      });
    },
    joinProject(project) {
      axios.post(`http://localhost:5000/projects/${project.id}/participate`, {}, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      })
      .then(response => {
        // 仅更新当前项目的消息
        project.message = response.data.message;
        // 设置消息显示3秒后清除
        setTimeout(() => {
          project.message = '';
        }, 3000);
      })
      .catch(error => {
        console.error("加入项目时出错: ", error);
        // 显示错误消息
        project.message = error.response ? error.response.data.message : "网络错误";
        // 设置消息显示3秒后清除
        setTimeout(() => {
          project.message = '';
        }, 3000);
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
  padding: 30px;
  background: linear-gradient(135deg, #e0f7fa, #ffffff);
  border-radius: 15px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.favorites-container:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

h2 {
  text-align: center;
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 30px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.favorites-list {
  list-style-type: none;
  padding: 0;
}

.project-card {
  background-color: #fff;
  margin-bottom: 20px;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: box-shadow 0.3s ease, transform 0.3s ease;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.5s forwards;
}

.project-card:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  transform: translateY(-5px);
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.project-created-by {
  font-size: 14px;
  color: #7f8c8d;
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.creator-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.creator-avatar:hover {
  transform: scale(1.1);
}

.project-link {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 16px;
  color: #3498db;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

.project-link:hover {
  color: #2980b9;
  text-decoration: underline;
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
  line-height: 1.6;
}

.images-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin-top: 10px;
}

.project-image {
  width: 100%;
  max-width: 150px;
  height: auto;
  object-fit: cover;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.project-image:hover {
  transform: scale(1.1);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.button-container {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
  margin-top: 10px;
}

.join-button, .favorite-button {
  padding: 10px 20px;
  font-size: 14px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.2s ease;
  font-weight: bold;
}

.join-button {
  background: linear-gradient(135deg, #42b983, #3ca772);
  color: #fff;
}

.join-button:hover {
  background: linear-gradient(135deg, #3ca772, #3498db);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.favorite-button {
  background: linear-gradient(135deg, #b2bec3, #95a5a6);
  color: #2d3436;
}

.favorite-button.favorited {
  background: linear-gradient(135deg, #d63031, #c0392b);
  color: #fff;
}

.favorite-button:hover {
  background: linear-gradient(135deg, #95a5a6, #7f8c8d);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.message {
  margin-top: 10px;
  color: #2c3e50;
  background-color: #e0f7fa;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
  font-weight: bold;
  opacity: 0;
  animation: fadeIn 0.3s forwards;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

</style>


