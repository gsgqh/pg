<template>
  <div class="projects-container">
    <h2>项目列表</h2>

    <!-- 筛选表单 -->
    <div class="filter-form">
      <select v-model="selectedCategory" class="select-field">
        <option value="">选择项目类别</option>
        <option value="项目">项目</option>
        <option value="竞赛">竞赛</option>
        <option value="科研">科研</option>
        <option value="学习">学习</option>
      </select>

      <select v-model="selectedMajorType" class="select-field">
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
    </div>

    <!-- 搜索表单 -->
    <div class="search-form">
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
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 20px;
}

.filter-form {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
  padding: 10px 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.select-field {
  flex: 1 1 200px;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
}

.search-form {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 30px;
  padding: 10px 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.search-input {
  flex: 2 1 300px;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-sizing: border-box;
}

.search-button {
  flex: 0 0 auto;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.search-button:hover {
  background-color: #2980b9;
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
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 20px;
  text-align: center;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.project-type:hover, .professional-type:hover {
  background-color: #e0e0e0;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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


