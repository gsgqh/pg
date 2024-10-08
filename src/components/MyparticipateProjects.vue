<template>
    <div class="projects-container">
      <h1 class="title">参与的项目</h1>
      <ul class="projects-list">
        <li v-for="project in projects" :key="project.id" class="project-card">
          <h2 class="project-title">{{ project.title }}</h2>
          <p class="project-content">{{ project.content }}</p>
  
          <div class="creator-info">
            <strong>项目创建者:</strong> 
            <router-link :to="'/user/' + project.username">{{ project.nickname }}</router-link>
          </div>
  
          <!-- 仅在项目有参与者时显示参与者列表 -->
          <div v-if="project.participants && project.participants.length" class="participants">
            <h3>参与者:</h3>
            <ul>
              <li v-for="participant in project.participants" :key="participant.id" class="participant-item">
                <div class="participant-info">
                  用户名: 
                  <router-link :to="'/user/' + participant.username">{{ participant.username }}</router-link> 
                  - 状态: {{ participant.status }}
                </div>
              </li>
            </ul>
          </div>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        projects: []
      };
    },
    created() {
      this.fetchProjects();
    },
    methods: {
      async fetchProjects() {
        try {
          const response = await axios.get('http://localhost:5000/my-participate-projects', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          });
          this.projects = response.data;
        } catch (error) {
          console.error('获取项目失败:', error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .projects-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    font-family: 'Arial', sans-serif;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  }
  
  .title {
    text-align: center;
    font-size: 28px;
    color: #2c3e50;
    margin-bottom: 20px;
  }
  
  .projects-list {
    list-style: none;
    padding: 0;
  }
  
  .project-card {
    padding: 20px;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    margin-bottom: 20px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  }
  
  .project-title {
    font-size: 24px;
    color: #2c3e50;
    margin: 0 0 10px;
  }
  
  .project-content {
    font-size: 16px;
    color: #34495e;
    margin-bottom: 10px;
  }
  
  .creator-info {
    margin-top: 10px;
    font-size: 16px;
    color: #2c3e50;
  }
  
  .participants {
    margin-top: 10px;
  }
  
  .participant-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 10px 0;
  }
  
  .participant-info {
    flex-grow: 1;
    text-align: center; /* 保持信息居中 */
  }
  </style>
  