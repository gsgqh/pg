<template>
    <div>
      <h2>Login</h2>
      <input v-model="loginUsername" placeholder="Username" />
      <input v-model="loginPassword" type="password" placeholder="Password" />
      <button @click="login">Login</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        loginUsername: '',
        loginPassword: ''
      };
    },
    methods: {
      login() {
        axios.post('http://localhost:5000/login', {
          username: this.loginUsername,
          password: this.loginPassword
        }).then(response => {
          localStorage.setItem('token', response.data.access_token);
          this.$router.push('/projects');  // 登录成功后跳转到项目列表
        });
      }
    }
  };
  </script>
  