<template>
    <div>
      <h2>Register</h2>
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button @click="register">Register</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        username: '',
        password: ''
      };
    },
    methods: {
      register() {
        axios.post('http://localhost:5000/register', {
          username: this.username,
          password: this.password
        }).then(() => {
          this.$router.push('/login');  // 注册成功后跳转到登录页面
        });
      }
    }
  };
  </script>
  