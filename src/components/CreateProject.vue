<template>
  <div>
    <h2>Create Project</h2>
    <input v-model="projectTitle" placeholder="Project Title" />
    <textarea v-model="projectContent" placeholder="Project Content"></textarea>
    <button @click="createProject">Create Project</button>
    
    <!-- 显示消息 -->
    <p v-if="successMessage" style="color: green;">{{ successMessage }}</p>
    <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
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
      // 清空之前的消息
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
          this.successMessage = response.data.message;  // 显示成功消息
          // 1.5秒后跳转
          setTimeout(() => {
            this.$router.push('/projects');
          }, 1500);
        }else{
          this.errorMessage = response.data.message;
        }
      })
      .catch(error => {
        if (error.response) {
          this.errorMessage = error.response.data.message;  // 显示错误消息
        } else {
          this.errorMessage = 'An error occurred while creating the project.';  // 通用错误消息
        }
      });
    }
  }
};
</script>
