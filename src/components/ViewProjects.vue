<template>
  <div>
    <h2>Projects</h2>
    <ul>
      <li v-for="project in projects" :key="project.id">
        <strong>Title:</strong> {{ project.title }} <br>
        <strong>Content:</strong> {{ project.content }} <br>
        <strong>Created by:</strong> {{ project.username }}
      </li>
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
    this.fetchProjects();  // 在组件挂载时获取项目数据
  }
};
</script>
