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

    <!-- 项目列表 -->
    <ul class="projects-list">
      <li v-for="project in projects" :key="project.id" class="project-card">
        <div class="project-header">
          <!-- 显示创建者头像 -->
          <img :src="project.creatorAvatar ? `/assets/${project.creatorAvatar}` : 'default-avatar.png'" alt="创建者头像" class="creator-avatar" />
          <router-link :to="'/user/' + project.username" class="project-link">
            {{ project.nickname }}
          </router-link>
        </div>

        <h3 class="project-title">{{ project.title }}</h3>
        <p class="project-content">{{ project.content }}</p>

        <div class="button-container">
          <button 
            @click="joinProject(project)" 
            class="join-button"
          >
            加入项目
          </button>

          <button 
            @click="toggleFavorite(project)" 
            class="favorite-button" 
            :class="{ favorited: project.isFavorited }"
          >
            {{ project.isFavorited ? '取消收藏' : '收藏' }}
          </button>
        </div>

        <div class="tag-container">
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

        <!-- 显示加入项目后的消息 -->
        <p v-if="project.message" class="message">{{ project.message }}</p>
      </li>
    </ul>

    <!-- 分页组件 -->
    <div class="pagination">
      <button 
        v-for="page in visiblePages" 
        :key="page" 
        @click="goToPage(page)" 
        :class="{ active: page === currentPage }"
      >
        {{ page }}
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

export default {
  name: 'ViewProjects',
  data() {
    return {
      projects: [],
      selectedCategory: '',
      selectedMajorType: '',
      searchKeyword: '',
      userId: null,
      currentPage: 1,  // 当前页数
      totalPages: 0,  // 总页数
      visiblePages: []  // 可见的页码数组
    };
  },
  methods: {
    fetchProjects() {
      const params = {
        page: this.currentPage  // 传递当前页码
      };

      axios.get('http://localhost:5000/projects', { params })
        .then(response => {
          return axios.get(`http://localhost:5000/users/${this.userId}/favorites`)
            .then(favoritesResponse => {
              const favoriteIds = new Set(favoritesResponse.data.map(fav => fav.id));
              this.totalPages = response.data.pages;  // 设置总页数
              this.projects = response.data.projects.map(project => ({
                ...project,
                isFavorited: favoriteIds.has(project.id),
                message: '',  // 初始化 message 属性
                creatorAvatar: project.avatar  // 处理头像数据
              }));
              this.updateVisiblePages();  // 更新可见的分页
            });
        })
        .catch(error => {
          console.error("获取项目时出错: ", error);
        });
    },
    searchProjects() {
      const params = {
        category: this.selectedCategory,
        major_type: this.selectedMajorType,
        keyword: this.searchKeyword,
        page: this.currentPage,  // 确保分页参数一起发送
      };

      axios.get('http://localhost:5000/projects/search', { params })
        .then(response => {
          return axios.get(`http://localhost:5000/users/${this.userId}/favorites`)
            .then(favoritesResponse => {
              const favoriteIds = new Set(favoritesResponse.data.map(fav => fav.id));
              this.totalPages = response.data.pages;  // 设置总页数
              this.projects = response.data.projects.map(project => ({
                ...project,
                isFavorited: favoriteIds.has(project.id),
                message: '',
                creatorAvatar: project.avatar
              }));
              this.updateVisiblePages();  // 更新分页
            });
        })
        .catch(error => {
          console.error("搜索项目时出错: ", error);
        });
    },
    selectCategory(category) {
      this.selectedCategory = category;
      this.searchProjects();
    },
    selectMajorType(majorType) {
      this.selectedMajorType = majorType;
      this.searchProjects();
    },
    toggleFavorite(project) {
      const action = project.isFavorited ? 'unfavorite' : 'favorite';
      axios.post(`http://localhost:5000/projects/${action}`, {
        user_id: this.userId,
        project_id: project.id
      })
      .then(() => {
        project.isFavorited = !project.isFavorited;
      })
      .catch(error => {
        console.error(`${project.isFavorited ? '取消收藏' : '收藏'}时出错: `, error);
      });
    },
    joinProject(project) {
      axios.post(`http://localhost:5000/projects/${project.id}/participate`, {}, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      })
      .then(response => {
        project.message = response.data.message;
        setTimeout(() => {
          project.message = '';
        }, 3000);
      })
      .catch(error => {
        console.error("加入项目时出错: ", error);
        project.message = error.response ? error.response.data.message : "网络错误";
        setTimeout(() => {
          project.message = '';
        }, 3000);
      });
    },
    goToPage(page) {
      if (page === '...') return;  // 忽略省略号
      this.currentPage = page;
      this.searchProjects();
    },
    updateVisiblePages() {
      // 确定要显示的页码，例如：1, ..., 5, 6, 7, ..., 9
      let start = Math.max(1, this.currentPage - 1);
      let end = Math.min(this.totalPages, this.currentPage + 1);

      this.visiblePages = [];

      if (start > 1) this.visiblePages.push(1);  // 总是显示第一页
      if (start > 2) this.visiblePages.push('...');  // 添加省略号

      for (let i = start; i <= end; i++) {
        this.visiblePages.push(i);
      }

      if (end < this.totalPages - 1) this.visiblePages.push('...');  // 添加省略号
      if (end < this.totalPages) this.visiblePages.push(this.totalPages);  // 总是显示最后一页
    }
  },
  watch: {
    selectedCategory: 'searchProjects',  // 当选中的项目类别改变时调用搜索
    selectedMajorType: 'searchProjects'   // 当选中的专业类型改变时调用搜索
  },
  mounted() {
    const token = localStorage.getItem('token');
    if (token) {
      const decodedToken = jwtDecode(token);
      this.userId = decodedToken.sub;  // 获取用户ID
    }
    this.fetchProjects();  // 获取项目数据
  }
};
</script>



<style scoped>
.projects-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Arial', sans-serif;
  background: linear-gradient(135deg, #e8f5e9, #ffffff);
  border-radius: 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

h2 {
  text-align: center;
  font-size: 32px;
  color: #2c3e50;
  margin-bottom: 20px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.filter-form, .search-form {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 20px;
  padding: 10px 20px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;
}

.filter-form:hover, .search-form:hover {
  transform: translateY(-2px);
}

.select-field, .search-input {
  flex: 1 1 200px;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-sizing: border-box;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.select-field:focus, .search-input:focus {
  border-color: #42b983;
  box-shadow: 0 0 8px rgba(66, 185, 131, 0.3);
}

.search-button {
  padding: 10px 20px;
  background-color: #3498db;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  font-weight: bold;
}

.search-button:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
}

.projects-list {
  list-style: none;
  padding: 0;
}

.project-card {
  padding: 20px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 12px;
  margin-bottom: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  position: relative;
  transition: box-shadow 0.3s ease, transform 0.3s ease;
  opacity: 0;
  transform: translateY(20px);
  animation: fadeInUp 0.5s forwards;
}

.project-card:hover {
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  transform: translateY(-5px);
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.project-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.creator-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
  object-fit: cover;
}

.project-link {
  font-size: 16px;
  color: #3498db;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

.project-link:hover {
  color: #2980b9;
  text-decoration: underline;
}

.project-title {
  font-size: 24px;
  color: #2c3e50;
  margin: 10px 0;
}

.project-content {
  font-size: 16px;
  color: #34495e;
  margin-bottom: 10px;
  line-height: 1.6;
}

.button-container {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 5px;
  margin-top: 10px;
}

.join-button, .favorite-button {
  padding: 8px 12px;
  background-color: #42b983;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  font-size: 14px;
}

.join-button:hover {
  background-color: #3ca772;
  transform: translateY(-2px);
}

.favorite-button {
  background-color: #b2bec3;
  color: #2d3436;
}

.favorite-button.favorited {
  background-color: #e74c3c;
  color: #fff;
}

.favorite-button:hover {
  background-color: #636e72;
  transform: translateY(-2px);
}

.tag-container {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.project-type,
.professional-type {
  padding: 8px 15px;
  border-radius: 8px;
  background-color: rgba(236, 240, 241, 0.8);
  cursor: pointer;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  font-size: 14px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.project-type:hover,
.professional-type:hover {
  background-color: rgba(189, 195, 199, 0.8);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
}

.message {
  margin-top: 10px;
  color: #2c3e50;
  background-color: #e0f7fa;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
  font-weight: bold;
  opacity: 0;
  animation: fadeIn 0.3s forwards;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>



