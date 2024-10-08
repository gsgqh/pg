<template>
  <div class="projects-container">
    <h1 class="title">参与的项目</h1>
    <ul class="projects-list">
      <li v-for="project in projects" :key="project.id" class="project-card">
        <h2 class="project-title">{{ project.title }}</h2>
        <p class="project-content">{{ project.content }}</p>
  
        <!-- 项目创建者信息 -->
        <div class="creator-info">
          <span class="creator-title">项目创建者:</span> 
          <router-link :to="'/user/' + project.nickname">
            <img :src="project.avatar ? `/assets/${project.avatar}` : 'default-avatar.png'" alt="创建者头像" class="creator-avatar" />
            {{ project.nickname }}</router-link>
        </div>
  
        <!-- 参与者信息，仅在项目有参与者时显示 -->
        <div v-if="project.participants && project.participants.length" class="participants">
          <h3 class="participants-title">参与者:</h3>
          <ul>
            <li v-for="participant in project.participants" :key="participant.id" class="participant-item">
              <div class="participant-info">
                用户  
                <router-link :to="'/user/' + participant.username">
                    <img :src="participant.avatar ? `/assets/${participant.avatar}` : 'default-avatar.png'" alt="参加者头像" class="creator-avatar" />
                    {{ participant.nickname }}</router-link> 
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
    padding: 30px;
    background: linear-gradient(135deg, #e0f7fa, #ffffff);
    border-radius: 15px;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
    font-family: 'Arial', sans-serif;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .projects-container:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  }
  
  .title {
    text-align: center;
    font-size: 32px;
    color: #2c3e50;
    margin-bottom: 20px;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
  }
  
  .projects-list {
    list-style: none;
    padding: 0;
  }
  
  .project-card {
    background-color: #fff;
    margin-bottom: 20px;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    position: relative;
    transition: box-shadow 0.3s ease, transform 0.3s ease;
    opacity: 0;
    transform: translateY(20px);
    animation: fadeInUp 0.5s forwards;
  }
  
  .project-card:hover {
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
    transform: translateY(-5px);
  }
  
  @keyframes fadeInUp {
    to {
      opacity: 1;
      transform: translateY(0);
    }
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
    line-height: 1.6;
  }
  
  .creator-info,
  .participants {
    margin-top: 15px;
    padding: 10px;
    background-color: #f8f9fa;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    font-size: 16px;
    color: #2c3e50;
  }
  
  .creator-title,
  .participants-title {
    font-size: 16px;
    color: #2c3e50;
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  .participants-title {
    text-align: left;
    padding-left: 5px;
  }
  
  .participant-item {
    display: flex;
    align-items: center;
    margin: 5px 0;
  }
  
  .participant-info,
  .creator-info {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  
  .participant-info img,
  .creator-info img {
    width: 35px;
    height: 35px;
    border-radius: 50%;
    object-fit: cover;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
  }
  
  .participant-info img:hover,
  .creator-info img:hover {
    transform: scale(1.1);
  }
  
  .participant-info .router-link,
  .creator-info .router-link {
    font-size: 16px;
    color: #3498db;
    font-weight: bold;
    text-decoration: none;
    transition: color 0.3s ease;
  }
  
  .participant-info .router-link:hover,
  .creator-info .router-link:hover {
    color: #2980b9;
    text-decoration: underline;
  }
  
  body::-webkit-scrollbar {
    width: 0; /* 隐藏滚动条 */
  }
  </style>
  
  
  

  