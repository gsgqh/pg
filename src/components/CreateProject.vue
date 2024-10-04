<template>
    <div>
      <h2>Create Project</h2>
      <input v-model="projectTitle" placeholder="Project Title" />
      <textarea v-model="projectContent" placeholder="Project Content"></textarea>
      <button @click="createProject">Create Project</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'CreateProject',
    data() {
      return {
        projectTitle: '',
        projectContent: ''
      };
    },
    methods: {
      createProject() {
        axios.post('http://localhost:5000/create-project', {
          title: this.projectTitle,
          content: this.projectContent
        }, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        }).then(() => {
          this.$router.push('/projects');  // 项目创建成功后跳转到项目列表
        });
      }
    }
  };
  </script>
  