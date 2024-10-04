<template>
    <div>
      <h2>Users List</h2>
      <ul v-if="users.length">
        <li v-for="user in users" :key="user.id">
          {{ user.username }}
        </li>
      </ul>
      <p v-else>No users found.</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'ViewUsers',
    data() {
      return {
        users: []
      };
    },
    mounted() {
      this.fetchUsers();
    },
    methods: {
      async fetchUsers() {
        try {
          const response = await axios.get('http://localhost:5000/users', {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
          });
          this.users = response.data;
        } catch (error) {
          console.error('Error fetching users:', error);
        }
      }
    }
  };
  </script>
  
  <style>
  /* 添加任何需要的样式 */
  </style>
  