<template>
  <div class="projects-container">
    <h1 class="title">项目管理</h1>
    <ul class="projects-list">
      <li v-for="project in projects" :key="project.id" class="project-card">
        <h2 class="project-title">{{ project.title }}</h2>
        <p class="project-content">{{ project.content }}</p>

        <div v-if="project.participants && project.participants.length" class="participants">
          <h3>参与者:</h3>
          <ul>
            <li v-for="participant in project.participants" :key="participant.id" class="participant-item">
              <div class="participant-info">
                用户名: 
                <router-link :to="'/user/' + participant.username">{{ participant.username }}</router-link> 
                - 状态: {{ participant.status }}
              </div>
              <div v-if="participant.status === '待审核'" class="review-buttons">
                <button @click="reviewParticipation(participant.id, 'approve')" class="approve-button">通过</button>
                <button @click="reviewParticipation(participant.id, 'reject')" class="reject-button">拒绝</button>
              </div>
            </li>
          </ul>
        </div>

        <div class="delete-container">
          <button 
            @click="confirmDelete(project.id)" 
            class="delete-button"
            :disabled="project.participants && project.participants.length"
          >
            删除项目
          </button>
          <span v-if="project.participants && project.participants.length" class="info-icon" title="无法删除：当前项目中有参与者或待审核申请。">ℹ️</span>
        </div>
      </li>
    </ul>

    <!-- 自定义弹窗 -->
    <div v-if="showConfirmDialog" class="confirm-dialog-overlay">
      <div class="confirm-dialog">
        <p>确定要删除该项目吗？</p>
        <div class="dialog-buttons">
          <button @click="deleteProject(confirmingProjectId)" class="confirm-button">确定</button>
          <button @click="closeDialog" class="cancel-button">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      projects: [],
      showConfirmDialog: false,
      confirmingProjectId: null
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
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.projects = response.data;
      } catch (error) {
        console.error('获取项目失败:', error);
      }
    },
    confirmDelete(projectId) {
      const project = this.projects.find(p => p.id === projectId);
      if (project.participants && project.participants.length > 0) {
        alert('无法删除项目：当前项目中有参与者或待审核申请。');
        return;
      }
      this.confirmingProjectId = projectId;
      this.showConfirmDialog = true;
    },
    async deleteProject(projectId) {
      try {
        const response = await axios.delete(`http://localhost:5000/delete-project/${projectId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (response.status === 200) {
          this.fetchProjects();
          this.closeDialog();
        } else {
          alert('删除项目失败！');
        }
      } catch (error) {
        alert('删除项目失败！');
        console.error('删除项目失败:', error);
      }
    },
    closeDialog() {
      this.showConfirmDialog = false;
      this.confirmingProjectId = null;
    },
    async reviewParticipation(participationId, action) {
      try {
        const response = await axios.post(`http://localhost:5000/participation/review/${participationId}`, 
        { 
          action: action
        }, 
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (response.status === 200) {
          alert(response.data.message);
          this.fetchProjects();
        } else {
          alert('审核操作失败！');
        }
      } catch (error) {
        alert('审核操作失败！');
        console.error('审核操作失败:', error);
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
  transition: box-shadow 0.3s ease, transform 0.3s ease;
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
  transition: box-shadow 0.3s ease, transform 0.3s ease;
  position: relative;
}

.project-card:hover {
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
  transform: translateY(-5px);
}

.delete-container {
  display: flex;
  align-items: center;
  justify-content: center; /* 居中对齐 */
  gap: 10px;
  margin-top: 10px;
}

.delete-button {
  background-color: #e74c3c;
  color: #fff;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.delete-button[disabled] {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.delete-button:hover:not([disabled]) {
  background-color: #c0392b;
  transform: translateY(-2px);
}

.info-icon {
  font-size: 18px;
  color: #3498db;
  cursor: pointer;
  transition: color 0.3s, transform 0.3s;
}

.info-icon:hover {
  color: #2980b9;
  transform: scale(1.2);
}

/* 自定义确认弹窗 */
.confirm-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.confirm-dialog {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
  max-width: 400px;
  margin: 0 auto;
}

.confirm-dialog p {
  font-size: 18px;
  color: #2c3e50;
  margin-bottom: 20px;
}

.dialog-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.confirm-button {
  background-color: #27ae60;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.confirm-button:hover {
  background-color: #219150;
}

.cancel-button {
  background-color: #e74c3c;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.cancel-button:hover {
  background-color: #c0392b;
}
</style>

