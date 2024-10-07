<template>
    <div class="favorites-container">
      <h2>我的收藏项目</h2>
      <ul class="favorites-list">
        <li v-for="project in favoriteProjects" :key="project.id" class="project-card">
          <h3 class="project-title">{{ project.title }}</h3>
          <p class="project-content">{{ project.content }}</p>
  
          <p class="project-created-by">
            <strong>创建者:</strong> 
            <router-link :to="'/user/' + project.username" class="project-link">
              {{ project.nickname }}
            </router-link>
          </p>
  
          <!-- 取消收藏按钮 -->
          <button 
            @click="toggleFavorite(project)" 
            class="favorite-button favorited"
          >
            取消收藏
          </button>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import {jwtDecode} from 'jwt-decode';  // 确保已经安装 jwt-decode 库
  
  export default {
    name: 'FavoriteProjects',
    data() {
      return {
        favoriteProjects: [],
        userId: null  // 初始化用户ID
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
        // 取消收藏
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
    },
    mounted() {
      const token = localStorage.getItem('token');
      if (token) {
        const decodedToken = jwtDecode(token);  // 解码 JWT
        this.userId = decodedToken.sub;  // 从 JWT 中获取当前用户的ID
      }
      this.fetchFavoriteProjects();  // 在组件挂载时获取收藏项目数据
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
  }
  
  .project-title {
    font-size: 22px;
    color: #333;
    margin-bottom: 10px;
  }
  
  .project-content {
    font-size: 16px;
    color: #555;
    margin-bottom: 15px;
  }
  
  .button-container {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
  }
  
  .project-type, .professional-type {
    padding: 10px 20px;
    background-color: #f0f0f0;
    border: 1px solid #ddd;
    border-radius: 20px;
    text-align: center;
    font-size: 14px;
    cursor: pointer;
  }
  
  .project-created-by {
    margin: 10px 0;
  }
  
  .project-link {
    color: #3498db;
    text-decoration: none;
  }
  
  .favorite-button {
    padding: 8px 15px;
    background-color: #e74c3c; /* 收藏状态按钮颜色 */
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }
  </style>
  