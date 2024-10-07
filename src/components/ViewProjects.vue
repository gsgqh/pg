<template>
  <div class="projects-container">
    <h2>项目列表</h2>
    <ul class="projects-list">
      <li v-for="project in projects" :key="project.id" class="project-card">
        <h3 class="project-title">{{ project.title }}</h3>
        <p class="project-content">{{ project.content }}</p>
        <p class="project-created-by">
          <strong>创建者:</strong> 
          <router-link :to="`/user/${project.username}`" class="project-link">
            {{ project.nickname }}
          </router-link>
        </p>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ViewProjects',
  data() {
    return {
      projects: []
    };
  },
  methods: {
    fetchProjects() {
      axios.get('http://localhost:5000/projects').then(response => {
        this.projects = response.data;
      });
    }
  },
  mounted() {
    this.fetchProjects();  // 在组件挂载时获取项目数据
  }
};
</script>

<style scoped>
.projects-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h2 {
  text-align: center;
  font-size: 28px;
  color: #2c3e50;
}

.projects-list {
  list-style-type: none;
  padding: 0;
}

.project-card {
  background-color: #fff;
  margin-bottom: 20px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.project-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
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

.project-created-by {
  font-size: 14px;
  color: #666;
}

.project-link {
  color: #3498db;
  text-decoration: none;
  font-weight: bold;
}

.project-link:hover {
  color: #2980b9;
  text-decoration: underline;
}
</style>
