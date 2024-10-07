<template>
  <div class="create-project-container">
    <h2 class="create-project-title">创建新项目</h2>
    <div class="form-container">
      <input
        v-model="projectTitle"
        placeholder="项目标题"
        class="input-field"
      />
      <textarea
        v-model="projectContent"
        placeholder="项目内容"
        class="input-field textarea-field"
      ></textarea>

      <select v-model="projectCategory" class="input-field select-category">
        <option disabled value="">请选择项目类别</option>
        <option>项目</option>
        <option>竞赛</option>
        <option>科研</option>
        <option>学习</option>
      </select>

      <select v-model="majorType" class="input-field select-major">
        <option disabled value="">请选择专业类型</option>
        <option>哲学</option>
        <option>经济学</option>
        <option>法学</option>
        <option>教育学</option>
        <option>文学</option>
        <option>历史学</option>
        <option>理学</option>
        <option>工学</option>
        <option>农学</option>
        <option>医学</option>
        <option>管理学</option>
        <option>艺术学</option>
      </select>

      <button @click="createProject" class="create-button">创建项目</button>

      <!-- 显示消息 -->
      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </div>
</template>



<script>
import axios from 'axios';

export default {
  name: 'CreateProject',
  data() {
    return {
      projectTitle: '',
      projectContent: '',
      projectCategory: '',
      majorType: '',
      successMessage: '',
      errorMessage: ''
    };
  },
  methods: {
    createProject() {
      this.successMessage = '';
      this.errorMessage = '';

      axios.post('http://localhost:5000/create-project', {
        title: this.projectTitle,
        content: this.projectContent,
        category: this.projectCategory,
        major_type: this.majorType
      }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      })
      .then(response => {
        if (response.data.success) {
          this.successMessage = response.data.message;
          setTimeout(() => {
            this.$router.push('/projects');
          }, 1500);
        } else {
          this.errorMessage = response.data.message;
        }
      })
      .catch(error => {
        if (error.response) {
          this.errorMessage = error.response.data.message;
        } else {
          this.errorMessage = 'An error occurred while creating the project.';
        }
      });
    }
  }
};
</script>


<style scoped>
.create-project-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 30px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
}

.create-project-title {
  text-align: center;
  font-size: 28px;
  color: #333;
  margin-bottom: 30px; /* 增加下方间距 */
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 20px; /* 为表单元素间增加默认的间距 */
}

.input-field {
  width: calc(100% - 40px); /* 留出左右各20px的边距 */
  padding: 14px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-sizing: border-box;
  transition: border-color 0.3s ease;
  margin: 0 20px; /* 增加左右边距 */
}

.input-field:focus {
  border-color: #3498db;
  outline: none;
}

.textarea-field {
  height: 150px;
  resize: vertical; /* 允许用户垂直调整文本域的大小 */
}

.create-button {
  width: calc(100% - 40px); /* 留出左右各20px的边距 */
  padding: 14px;
  font-size: 16px;
  color: #fff;
  background-color: #42b983;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
  margin: 0 20px; /* 增加左右边距 */
}

.create-button:hover {
  background-color: #3ca772;
  transform: translateY(-2px);
}

.create-button:active {
  background-color: #3498db;
  transform: translateY(0);
}

.success-message, .error-message {
  font-size: 14px;
  margin-top: 10px;
  text-align: center;
}

.success-message {
  color: #28a745; /* 绿色，用于成功消息 */
}

.error-message {
  color: #dc3545; /* 红色，用于错误消息 */
}
</style>


