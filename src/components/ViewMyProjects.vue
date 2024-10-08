<template>
  <div class="projects-container">
    <h1 class="title">项目管理</h1>

    <ul class="projects-list">
      <li v-for="project in projects" :key="project.id" class="project-card">
        <h2 class="project-title">{{ project.title }}</h2>
        <p class="project-content">{{ project.content }}</p>

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

              <!-- 仅在状态为 '待审核' 时显示操作按钮 -->
              <div v-if="participant.status === '待审核'" class="review-buttons">
                <button @click="reviewParticipation(participant.id, 'approve')" class="approve-button">通过</button>
                <button @click="reviewParticipation(participant.id, 'reject')" class="reject-button">拒绝</button>
              </div>
            </li>
          </ul>

          <!-- 添加公告输入框 -->
          <div class="announcement-container">
            <h3>发布公告</h3>
            <textarea v-model="announcementMessage[project.id]" placeholder="输入公告内容..." rows="4"></textarea>
            <button @click="publishAnnouncement(project.id)" class="publish-button">发布公告</button>
          </div>
        </div>

        <button 
          @click="deleteProject(project.id)" 
          class="delete-button"
          :disabled="project.participants && project.participants.length"
        >
          删除项目
        </button>

        <!-- 使用图标或文本提示删除限制 -->
        <p v-if="project.participants && project.participants.length" class="delete-warning">
          <span class="info-icon" title="无法删除：当前项目中有参与者或待审核申请。">ℹ️</span>
        </p>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      projects: [],
      announcementMessage: {}  // 新增，使用对象存储每个项目的公告消息
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
    async deleteProject(projectId) {
      const project = this.projects.find(p => p.id === projectId);

      if (project.participants && project.participants.length > 0) {
        alert('无法删除项目：当前项目中有参与者或待审核申请。');
        return;
      }

      if (confirm('确定要删除该项目吗？')) {
        try {
          const response = await axios.delete(`http://localhost:5000/delete-project/${projectId}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          });
          if (response.status === 200) {
            this.fetchProjects();
          } else {
            alert('删除项目失败！');
          }
        } catch (error) {
          alert('删除项目失败！');
          console.error('删除项目失败:', error);
        }
      }
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
    },
    async publishAnnouncement(projectId) {
      const message = this.announcementMessage[projectId];

      if (!message) {
        alert('公告内容不能为空！');
        return;
      }

      try {
        const response = await axios.post(`http://localhost:5000/projects/${projectId}/announce`, 
        { 
          message: message 
        }, 
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (response.status === 200) {
          alert('公告发布成功！');
          this.announcementMessage[projectId] = '';  // 清空对应项目的输入框
        } else {
          alert('公告发布失败！');
        }
      } catch (error) {
        alert('公告发布失败！');
        console.error('公告发布失败:', error);
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

.participant-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 10px 0;
}

.participant-info {
  flex-grow: 1;
  text-align: center;
}

.review-buttons {
  display: flex;
  gap: 10px;
}

.approve-button {
  background-color: #27ae60;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.approve-button:hover {
  background-color: #219150;
}

.reject-button {
  background-color: #e74c3c;
  color: #fff;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.reject-button:hover {
  background-color: #c0392b;
}

.delete-button {
  padding: 10px 15px;
  background-color: #e74c3c;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 15px;
}

.delete-button[disabled] {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.delete-button:hover:not([disabled]) {
  background-color: #c0392b;
}

.delete-warning {
  color: #e74c3c;
  font-size: 14px;
  margin-top: 5px;
  display: flex;
  align-items: center;
}

.info-icon {
  cursor: pointer;
  margin-left: 5px;
}

/* 添加公告相关的样式 */
.announcement-container {
  margin-top: 20px;
}

textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  resize: none;
}

.publish-button {
  margin-top: 10px;
  padding: 10px 15px;
  background-color: #3498db;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.publish-button:hover {
  background-color: #2980b9;
}
</style>
