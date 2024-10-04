<template>
    <div>
      <h2>Projects</h2>
      <ul>
        <li v-for="project in projects" :key="project.id">{{ project.title }}</li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'ViewProjects',
    data() {
      return {
        projects: []
      };
    },
    methods: {
      fetchProjects() {
        axios.get('http://localhost:5000/projects').then(response => {
          this.projects = response.data;
        });
      }
    },
    mounted() {
      this.fetchProjects();
    }
  };
  </script>
  