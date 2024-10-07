<template>
  <div class="projects-container">
    <h2>项目列表</h2>

    <!-- 搜索表单 -->
    <div class="search-form">
      <select v-model="selectedCategory">
        <option value="">选择项目类别</option>
        <option value="项目">项目</option>
        <option value="竞赛">竞赛</option>
        <option value="科研">科研</option>
        <option value="学习">学习</option>
      </select>

      <select v-model="selectedMajorType">
        <option value="">选择专业类型</option>
        <option value="哲学">哲学</option>
        <option value="经济学">经济学</option>
        <option value="法学">法学</option>
        <option value="教育学">教育学</option>
        <option value="文学">文学</option>
        <option value="历史学">历史学</option>
        <option value="理学">理学</option>
        <option value="工学">工学</option>
        <option value="农学">农学</option>
        <option value="医学">医学</option>
        <option value="管理学">管理学</option>
        <option value="艺术学">艺术学</option>
      </select>

      <!-- 搜索栏 -->
      <input
        type="text"
        v-model="searchKeyword"
        placeholder="搜索项目标题和内容"
        class="search-input"
      />
      <button @click="searchProjects" class="search-button">搜索</button>
    </div>

    <ul class="projects-list">
      <li v-for="project in projects" :key="project.id" class="project-card">
        <h3 class="project-title">{{ project.title }}</h3>
        <p class="project-content">{{ project.content }}</p>

        <!-- 项目类别和专业类型按钮 -->
        <div class="button-container">
          <div 
            class="project-type" 
            @click="selectCategory(project.category)"
          >
            {{ project.category }}
          </div>
          <div 
            class="professional-type" 
            @click="selectMajorType(project.major_type)"
          >
            {{ project.major_type }}
          </div>
        </div>

        <p class="project-created-by">
          <strong>创建者:</strong> 
          <router-link :to="'/user/' + project.username" class="project-link">
            {{ project.nickname }}
          </router-link>
        </p>
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
      projects: [],
      selectedCategory: '',  // 存储用户选择的项目类别
      selectedMajorType: '',  // 存储用户选择的专业类型
      searchKeyword: ''  // 存储搜索关键字
    };
  },
  methods: {
    fetchProjects() {
      axios.get('http://localhost:5000/projects').then(response => {
        this.projects = response.data;
      });
    },
    searchProjects() {
      // 构建查询参数
      const params = {
        category: this.selectedCategory,
        major_type: this.selectedMajorType,
        keyword: this.searchKeyword  // 将关键字添加到查询参数中
      };

      // 发送带有查询参数的请求
      axios.get('http://localhost:5000/projects/search', { params })
        .then(response => {
          this.projects = response.data;
        })
        .catch(error => {
          console.error("搜索项目时出错: ", error);
        });
    },
    selectCategory(category) {
      this.selectedCategory = category; // 设置选中的项目类别
      this.searchProjects(); // 自动搜索
    },
    selectMajorType(majorType) {
      this.selectedMajorType = majorType; // 设置选中的专业类型
      this.searchProjects(); // 自动搜索
    }
  },
  watch: {
    selectedCategory: 'searchProjects',  // 当选中的项目类别改变时调用搜索
    selectedMajorType: 'searchProjects'   // 当选中的专业类型改变时调用搜索
  },
  mounted() {
    this.fetchProjects();  // 在组件挂载时获取项目数据
  }
};
</script>

<style scoped>
.projects-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

h2 {
  text-align: center;
  font-size: 28px;
  color: #2c3e50;
}

.search-form {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

select {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.search-input {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 200px; /* 搜索框的宽度 */
}

.search-button {
  padding: 10px 15px;
  font-size: 16px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.search-button:hover {
  background-color: #2980b9; /* 悬停效果 */
}

.projects-list {
  list-style-type: none;
  padding: 0;
}

.project-card {
  background-color: #fff;
  margin-bottom: 20px;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.project-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.project-title {
  font-size: 22px;
  color: #333;
  margin-bottom: 10px;
}

.project-content {
  font-size: 16px;
  color: #555;
  margin-bottom: 15px;
}

.button-container {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}

.project-type, .professional-type {
  padding: 10px 20px;
  background-color: white;
  border: 1px solid black;
  border-radius: 12px;
  text-align: center;
  font-size: 14px;
  cursor: pointer;  /* 添加手形光标以指示可点击 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.project-type:hover, .professional-type:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* 悬停效果 */
}

.project-created-by {
  font-size: 14px;
  color: #666;
}

.project-link {
  color: #3498db;
  text-decoration: none;
  font-weight: bold;
}

.project-link:hover {
  color: #2980b9;
  text-decoration: underline;
}
</style>
