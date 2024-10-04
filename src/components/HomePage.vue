<template>
    <div>
      <h1>Welcome to the Project Demo</h1>
      <button @click="goToRegister">Register</button>
      <button @click="goToLogin">Login</button>
      <button @click="goToCreateProject">Create Project</button>
      <button @click="goToViewProjects">View Projects</button>
    </div>
  </template>
  
  <script>
  export default {
    name: 'HomePage',
    methods: {
      goToRegister() {
        this.$router.push('/register');
      },
      goToLogin() {
        this.$router.push('/login');
      },
      goToCreateProject() {
        this.$router.push('/create-project');
      },
      goToViewProjects() {
        this.$router.push('/projects');
      }
    }
  }
  </script>
  
  <style>
  button {
    margin: 10px;
    padding: 10px;
    font-size: 16px;
  }
  </style>
  