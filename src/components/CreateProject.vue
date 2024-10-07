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
      successMessage: '',  // 用于存储成功消息
      errorMessage: ''     // 用于存储错误消息
    };
  },
  methods: {
    createProject() {
      this.successMessage = '';
      this.errorMessage = '';

      axios.post('http://localhost:5000/create-project', {
        title: this.projectTitle,
        content: this.projectContent
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
  padding: 20px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
}

.create-project-title {
  text-align: center;
  font-size: 28px;
  color: #333;
  margin-bottom: 20px;
}

.form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.input-field {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-sizing: border-box;
  transition: border-color 0.3s ease;
}

.input-field:focus {
  border-color: #3498db;
  outline: none;
}

.textarea-field {
  height: 120px;
}

.create-button {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  color: white;
  background-color: #42b983;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.create-button:hover {
  background-color: #3ca772;
  transform: translateY(-2px);
}

.create-button:active {
  background-color: #3498db;
  transform: translateY(0);
}

.success-message {
  color: green;
  margin-top: 15px;
}

.error-message {
  color: red;
  margin-top: 15px;
}
</style>
