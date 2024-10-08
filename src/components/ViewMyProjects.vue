<template>
  <!-- 背景容器 -->
  <div class="particles-background"></div>

  <div class="projects-container">
    <h1 class="title">项目管理</h1>
    <ul class="projects-list">
      <li v-for="project in projects" :key="project.id" class="project-card">
        <div v-if="!project.isEditing">
          <h2 class="project-title">{{ project.title }}</h2>
          <p class="project-content">{{ project.content }}</p>
          <p class="project-status">状态: {{ project.status }}</p> <!-- 显示项目状态 -->
          <button @click="editProject(project)" class="edit-button" :disabled="hasPendingParticipants(project)" >编辑</button>
          <span v-if="hasPendingParticipants(project)" class="info-icon" title="请先处理当前的申请。">ℹ️</span>
        </div>

        <div v-else>
          <input 
            v-model="project.title" 
            class="edit-title-input" 
            placeholder="编辑标题"
          />
          <textarea 
            v-model="project.content" 
            class="edit-content-input" 
            placeholder="编辑内容"
          ></textarea>
          
          <div class="review-buttons">
            <button 
              @click="updateStatus(project, '招募中')" 
              :class="{ 'active': project.status === '招募中' }"
            >
              招募中
            </button>
            <button 
              @click="updateStatus(project, '进行中')" 
              :class="{ 'active': project.status === '进行中' }"
            >
              进行中
            </button>
            <button 
              @click="updateStatus(project, '已结束')" 
              :class="{ 'active': project.status === '已结束' }"
            >
              已结束
            </button>
          </div>
          
          <button @click="submitEdit(project)" class="submit-button">提交</button>
        </div>

        <!-- 添加项目图片显示 -->
        <div class="images-container">
          <img 
            v-for="(image, index) in project.images" 
            :key="index" 
            :src="`${image}`" 
            alt="项目图片" 
            class="project-image" 
            @click="viewImage(project, image)"
          />
        </div>

        <!-- 图片查看器弹窗 -->
        <div v-if="project.showImageViewer" class="image-viewer-overlay" @click="closeImageViewer(project)">
          <img :src="project.currentImage" class="image-viewer" alt="查看图片" />
        </div>

        <!-- 参与者和公告部分... -->
        <div v-if="project.participants && project.participants.length" class="participants">
          <h3 class="participant-title">参与者:</h3>
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

          <div class="announce-container">
            <input 
              v-model="announcementMessage" 
              placeholder="输入公告内容..." 
              class="announcement-input"
            />
            <button @click="publishAnnouncement(project.id)" class="announce-button">发布公告</button>
          </div>
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
      confirmingProjectId: null,
      announcementMessage: ''  // 新增：存储公告内容
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
        this.projects = response.data.map(project => ({
          ...project,
          isEditing: false, // 新增字段，用于控制编辑状态
          showImageViewer: false, // 新增字段，用于控制图片查看器状态
          currentImage: '' // 新增字段，用于存储当前查看的图片
        }));
      } catch (error) {
        console.error('获取项目失败:', error);
      }
    },
    editProject(project) {
      // 检查是否有待审核的参与者
      if (this.hasPendingParticipants(project)) {
        alert('请先处理当前的申请。');
        return;
      }
      project.isEditing = true;  // 切换到编辑模式
    },
    async submitEdit(project) {
      try {
        const response = await axios.put(`http://localhost:5000/edit-project/${project.id}`, {
          title: project.title,
          content: project.content,
          status: project.status // 发送状态
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (response.status === 200) {
          project.isEditing = false;  // 提交成功后退出编辑模式
          this.fetchProjects();  // 刷新项目列表
        } else {
          alert('更新项目失败！');
        }
      } catch (error) {
        alert('更新项目失败！');
        console.error('更新项目失败:', error);
      }
    },
    updateStatus(project, newStatus) {
      project.status = newStatus; // 更新状态
    },
    hasPendingParticipants(project) {
      // 检查是否有参与者的状态为待审核
      return project.participants && project.participants.some(participant => participant.status === '待审核');
    },
    viewImage(project, image) {
      project.currentImage = image; // 设置当前项目的图片
      project.showImageViewer = true; // 显示该项目的图片查看器
    },
    closeImageViewer(project) {
      project.showImageViewer = false; // 关闭该项目的图片查看器
      project.currentImage = ''; // 清空当前图片
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
    async publishAnnouncement(projectId) {
      if (!this.announcementMessage) {
        alert('公告内容不能为空！');
        return;
      }

      try {
        const response = await axios.post(`http://localhost:5000/projects/${projectId}/announce`, {
          message: this.announcementMessage
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });

        if (response.status === 200) {
          alert(response.data.message);
          this.announcementMessage = ''; // 清空文本框
          this.fetchProjects(); // 重新获取项目
        } else {
          alert('公告发布失败！');
        }
      } catch (error) {
        alert('公告发布失败: ' + error.response.data.message);
        console.error('公告发布失败:', error);
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
    }
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

.projects-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
  background: linear-gradient(135deg, #e0f7fa, #ffffff);
  border-radius: 15px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease, transform 0.3s ease;
  position: relative;
  z-index: 1; /* 确保内容在背景上方 */
}

.title {
  text-align: center;
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 20px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.projects-list {
  list-style: none;
  padding: 0;
}

.project-card {
  padding: 20px;
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid #ddd;
  border-radius: 12px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.project-card:hover {
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
  transform: translateY(-5px);
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

.participants {
  margin-top: 15px;
}

.participant-title {
  font-size: 16px;
  color: #2c3e50;
  margin-bottom: 10px;
  font-weight: bold;
}

.participant-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(240, 248, 255, 0.6);
  padding: 10px;
  border-radius: 8px;
  margin-bottom: 10px;
}

.participant-info {
  flex: 1;
  text-align: center;
  font-size: 14px;
  color: #2c3e50;
}

.review-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.approve-button, .reject-button {
  background-color: #27ae60;
  color: #fff;
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
  font-size: 14px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.reject-button {
  background-color: #e74c3c;
}

.approve-button:hover {
  background-color: #2ecc71;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.reject-button:hover {
  background-color: #e57373;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.approve-button:active, .reject-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.delete-container {
  display: flex;
  align-items: center;
  justify-content: center;
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
  background: #ffffff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);
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
  border-radius: 8px;
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
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.cancel-button:hover {
  background-color: #c0392b;
}

.announce-container {
  margin-top: 10px;
}

.announcement-input {
  width: 70%;
  padding: 8px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.announcement-input:focus {
  border-color: #3498db;
  box-shadow: 0 0 8px rgba(52, 152, 219, 0.3);
}

.announce-button {
  background-color: #27ae60;
  color: #fff;
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s ease;
}

.announce-button:hover {
  background-color: #219150;
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

body::-webkit-scrollbar {
  width: 0;
}

.edit-title-input, .edit-content-input {
  width: 100%;
  margin: 10px 0;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.submit-button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
}

.submit-button:hover {
  background-color: #218838;
}

.edit-button{
  background-color: #287fa7;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
}

.edit-button:hover {
  background-color: #287fa7;
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
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5);
  transition: transform 0.3s ease;
}

.review-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-bottom: 15px; /* 增加按钮组与提交按钮之间的间距 */
}

.review-buttons button {
  background-color: #27ae60;
  color: #fff;
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.3s ease;
  font-size: 14px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.review-buttons .reject-button {
  background-color: #e74c3c;
}

.review-buttons button.active {
  background-color: #2ecc71; /* 激活状态的按钮颜色 */
}

.edit-button[disabled] {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.edit-button:hover:not([disabled]) {
  background-color: #c0392b;
  transform: translateY(-2px);
}

.submit-button {
  margin-top: 10px; /* 增加提交按钮的顶部边距 */
}

</style>

