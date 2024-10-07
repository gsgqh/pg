<template>
  <div class="projects-container">
    <h1 class="title">项目管理</h1>
    <ul class="projects-list">
      <li v-for="project in projects" :key="project.id" class="project-card">
        <h2 class="project-title">{{ project.title }}</h2>
        <p class="project-content">{{ project.content }}</p>
        <div class="participants">
          <h3>参与者:</h3>
          <ul>
            <li v-for="participant in project.participants" :key="participant.id">
              用户名: <router-link :to="'/user/' + participant.username">{{ participant.username }}</router-link> - 状态: {{ participant.status }}
              <button @click="reviewParticipation(participant.id, 'approve')">通过</button>
              <button @click="reviewParticipation(participant.id, 'reject')">拒绝</button>
            </li>
          </ul>
        </div>
        
        <button @click="deleteProject(project.id)" class="delete-button">删除项目</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios'; // Importing Axios

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
        const response = await axios.get('http://localhost:5000/projects/my-projects', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}` // 使用 JWT 进行认证
          }
        });
        this.projects = response.data; // Assigning data from the response
      } catch (error) {
        console.error('获取项目失败:', error); // Logging error
      }
    },
    async deleteProject(projectId) {
      if (confirm('确定要删除该项目吗？')) {
        try {
          const response = await axios.delete(`http://localhost:5000/delete-project/${projectId}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}` // 使用 JWT 进行认证
            }
          });
          if (response.status === 200) {
            this.fetchProjects(); // Refresh project list
          } else {
            alert('删除项目失败！');
          }
        } catch (error) {
          alert('删除项目失败！');
          console.error('删除项目失败:', error); // Logging error
        }
      }
    },
    async reviewParticipation(participationId, action) {
      try {
        const response = await axios.post(`http://localhost:5000/participation/review/${participationId}`, 
        { 
          action: action  // 只发送 action
        }, 
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`  // 使用 JWT 进行认证
          }
        });
    
        if (response.status === 200) {
          alert(response.data.message);  // 提示操作结果
          this.fetchProjects();  // 刷新项目列表
        } else {
          alert('审核操作失败！');
        }
      } catch (error) {
        alert('审核操作失败！');
        console.error('审核操作失败:', error);  // 打印错误日志
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

.participants {
  margin-top: 10px;
}

.delete-button {
  padding: 10px 15px;
  background-color: #e74c3c;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.delete-button:hover {
  background-color: #c0392b;
}
</style>
