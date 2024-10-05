<template>
  <div id="app">
    <h1>Project Demo</h1>
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/register">Register</router-link> |
      <router-link to="/login">Login</router-link> |
      <router-link to="/create-project">Create Project</router-link> |
      <router-link to="/projects">View Projects</router-link> |
      <router-link to="/users">View Users</router-link> |
      <router-link to="/profile">My Profile</router-link> |
      <router-link to="/edit-profile">edit Profile</router-link>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App'
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
nav {
  margin-bottom: 20px;
}
</style>
