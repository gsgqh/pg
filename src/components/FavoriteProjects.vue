<template>
  <!-- 背景容器 -->
  <div class="particles-background"></div>

  <!-- 收藏项目容器 -->
  <div class="favorites-container">
    <h2>我的收藏项目</h2>
    <ul class="favorites-list">
      <li v-for="project in favoriteProjects" :key="project.id" class="project-card">
        <div class="project-created-by">
          <router-link :to="'/user/' + project.username" class="project-link">
            <img :src="project.avatar ? require(`@/assets/${project.avatar}`) : 'default-avatar.png'" alt="创建者头像" class="creator-avatar" />
            <span>{{ project.nickname }}</span>
          </router-link>
        </div>
        <h3 class="project-title">{{ project.title }}</h3>
        <p class="project-content">{{ project.content }}</p>

        <!-- 项目图片容器，点击图片查看大图 -->
        <div class="images-container">
          <img 
            v-for="(image, index) in project.images" 
            :key="index" 
            :src="image" 
            alt="项目图片" 
            class="project-image"
            @click="viewImage(image)"
          />
        </div>

        <!-- 项目状态 -->
        <p class="project-status">状态: {{ project.status }}</p> <!-- 新增项目状态 -->


        <div class="button-container">
          <button @click="joinProject(project)" class="join-button">加入项目</button>
          <button @click="toggleFavorite(project)" class="favorite-button" :class="{ favorited: project.isFavorited }">取消收藏</button>
        </div>
        <p v-if="project.message" class="message">{{ project.message }}</p>
      </li>
    </ul>

    <!-- 图片查看器弹窗 -->
    <div v-if="showImageViewer" class="image-viewer-overlay" @click="closeImageViewer">
      <img :src="currentImage" class="image-viewer" alt="查看图片" />
    </div>
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
      showImageViewer: false, // 控制图片查看器的显示
      currentImage: '' // 当前查看的图片 URL
    };
  },
  methods: {
    fetchFavoriteProjects() {
      axios.get(`http://localhost:5000/users/${this.userId}/favorites`)
        .then(response => {
          this.favoriteProjects = response.data.map(project => ({
            ...project,
            message: '' // 初始化 message 属性
          }));
        })
        .catch(error => {
          console.error("获取收藏项目时出错: ", error);
        });
    },
    viewImage(image) {
      this.currentImage = image;
      this.showImageViewer = true;
    },
    closeImageViewer() {
      this.showImageViewer = false;
      this.currentImage = '';
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
    joinProject(project) {
      axios.post(`http://localhost:5000/projects/${project.id}/participate`, {}, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      })
      .then(response => {
        project.message = response.data.message;
        setTimeout(() => {
          project.message = '';
        }, 3000);
      })
      .catch(error => {
        console.error("加入项目时出错: ", error);
        project.message = error.response ? error.response.data.message : "网络错误";
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
/* 粒子背景样式 */
.particles-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(-45deg, #1e3c72, #2a5298, #e8f5e9, #ffffff);
  background-size: 400% 400%;
  animation: gradientAnimation 15s ease infinite;
  z-index: -1; /* 确保背景在所有内容的后面 */
}

@keyframes gradientAnimation {
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

/* 收藏项目容器样式 */
.favorites-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 30px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 15px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  position: relative;
  z-index: 1;
}

h2 {
  text-align: center;
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 30px;
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
  transition: box-shadow 0.3s ease, transform 0.3s ease;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.5s forwards;
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.project-header {
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
}

.project-link:hover {
  color: #2980b9;
  text-decoration: underline;
}

.project-title {
  font-size: 22px;
  color: #2c3e50;
  margin-bottom: 10px;
}

.project-content {
  font-size: 16px;
  color: #34495e;
  margin-bottom: 15px;
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
  transition: transform 0.3s ease;
}

.project-image:hover {
  transform: scale(1.1);
}

.image-viewer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.image-viewer {
  max-width: 90%;
  max-height: 90%;
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
}

.button-container {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 10px;
}

.join-button,
.favorite-button {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
}

.join-button {
  background: linear-gradient(135deg, #42b983, #3ca772);
  color: #fff;
}

.favorite-button {
  background: linear-gradient(135deg, #b2bec3, #95a5a6);
  color: #2d3436;
}

.favorite-button.favorited {
  background: linear-gradient(135deg, #d63031, #c0392b);
  color: #fff;
}

.message {
  margin-top: 10px;
  background-color: #e0f7fa;
  padding: 10px;
  border-radius: 5px;
  text-align: center;
}
</style>
