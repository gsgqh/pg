<template>
  <!-- 背景容器 -->
  <div class="particles-background"></div>

  <!-- 项目列表容器 -->
  <div class="projects-container">
    <h1 class="title">参与的项目</h1>
    <ul class="projects-list">
      <li v-for="project in projects" :key="project.id" class="project-card">
        <h2 class="project-title">{{ project.title }}</h2>
        <p class="project-content">{{ project.content }}</p>

        <!-- 项目图片容器，点击图片查看大图 -->
        <div class="images-container">
          <img 
            v-for="(image, index) in project.images" 
            :key="index" 
            :src="image" 
            alt="项目图片" 
            class="project-image"
            @click="viewImage(project, image)"
          />
        </div>
        
        <!-- 图片查看器弹窗 -->
        <div v-if="project.showImageViewer" class="image-viewer-overlay" @click="closeImageViewer(project)">
          <img :src="project.currentImage" class="image-viewer" alt="查看图片" />
        </div>

        <!-- 项目创建者信息 -->
        <div class="creator-info">
          <span class="creator-title">项目创建者:</span>
          <router-link :to="'/user/' + project.nickname" class="creator-link">
            <img :src="project.avatar ? require(`@/assets/${project.avatar}`) : 'default-avatar.png'" alt="创建者头像" class="creator-avatar" />
            <span>{{ project.nickname }}</span>
          </router-link>
        </div>
  
        <!-- 参与者信息，仅在项目有参与者时显示 -->
        <div v-if="project.participants && project.participants.length" class="participants">
          <h3 class="participants-title">参与者:</h3>
          <ul>
            <li v-for="participant in project.participants" :key="participant.id" class="participant-item">
              <div class="participant-info">
                <router-link :to="'/user/' + participant.username" class="participant-link">
                  <img :src="participant.avatar ? require(`@/assets/${participant.avatar}`) : 'default-avatar.png'" alt="参加者头像" class="creator-avatar" />
                  <span>{{ participant.nickname }}</span>
                </router-link>
                <span class="participant-status">- 状态: {{ participant.status }}</span>
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
      projects: [], // 项目列表
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

        // 为每个项目添加状态管理属性
        this.projects = response.data.map(project => ({
          ...project,
          showImageViewer: false, // 初始化图片查看器状态
          currentImage: '' // 初始化当前图片
        }));
      } catch (error) {
        console.error('获取项目失败:', error);
      }
    },
    viewImage(project, image) {
      project.currentImage = image; // 设置当前项目的图片
      project.showImageViewer = true; // 显示该项目的图片查看器
    },
    closeImageViewer(project) {
      project.showImageViewer = false; // 关闭该项目的图片查看器
      project.currentImage = ''; // 清空当前图片
    }
  }
};
</script>

  
  <style scoped>
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

.projects-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 30px;
  background: linear-gradient(135deg, #e0f7fa, #ffffff);
  border-radius: 15px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
  transition: transform 0.3s ease, box-shadow 0.3s ease;  
  position: relative;
  z-index: 1;
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
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.project-card:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  transform: translateY(-5px);
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

.images-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  margin-top: 10px;
}

.project-image {
  width: 100%;
  max-width: 150px; /* 设置最大宽度 */
  height: auto; /* 高度自动调整 */
  object-fit: cover; /* 保持图片比例 */
  border-radius: 8px; /* 圆角 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* 阴影效果 */
  transition: transform 0.3s ease, box-shadow 0.3s ease; /* 平滑过渡效果 */
}

.project-image:hover {
  transform: scale(1.1); /* 悬停时放大 */
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* 加强阴影 */
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
  margin: 5px 0;
}

.participant-info,
.creator-link {
  display: flex;
  align-items: center;
  gap: 10px;
}

.creator-link {
  text-decoration: none;
  color: #3498db;
  font-weight: bold;
  transition: color 0.3s ease;
}

.creator-link:hover {
  color: #2980b9;
  text-decoration: underline;
}

.creator-avatar {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.creator-avatar:hover {
  transform: scale(1.1); /* 悬停时放大 */
}

.participant-link {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #3498db;
  font-weight: bold;
  text-decoration: none;
  transition: color 0.3s ease;
}

.participant-link:hover {
  color: #2980b9;
  text-decoration: underline;
}

.participant-status {
  margin-left: 10px;
  color: #555;
  font-size: 14px;
}

body::-webkit-scrollbar {
  width: 0;
}

/* 图片查看器样式 */
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
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  transition: transform 0.3s ease;
}
</style>

  
  
  

  