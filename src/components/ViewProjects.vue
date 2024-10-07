<template>
  <div class="projects-container">
    <h2>项目列表</h2>

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

        <button 
          @click="toggleFavorite(project)" 
          class="favorite-button" 
          :class="{ favorited: project.isFavorited }"
        >
          {{ project.isFavorited ? '取消收藏' : '收藏' }}
        </button>

        <button 
          @click="joinProject(project.id)" 
          class="join-button"
        >
          加入项目
        </button>
        <p v-if="message" class="message">{{ message }}</p> <!-- 添加这一行 -->
      </li>
    </ul>
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
      userId: null,  // 初始化为 null
      message: ''    // 添加消息状态
    };
  },
  methods: {
    fetchProjects() {
      axios.get('http://localhost:5000/projects').then(response => {
        return axios.get(`http://localhost:5000/users/${this.userId}/favorites`).then(favoritesResponse => {
          const favoriteIds = new Set(favoritesResponse.data.map(fav => fav.id));
          this.projects = response.data.map(project => ({
            ...project,
            isFavorited: favoriteIds.has(project.id)  // 根据用户的收藏状态设置 isFavorited
          }));
        });
      }).catch(error => {
        console.error("获取项目时出错: ", error);
      });
    },
    searchProjects() {
      const params = {
        category: this.selectedCategory,
        major_type: this.selectedMajorType,
        keyword: this.searchKeyword
      };

      axios.get('http://localhost:5000/projects/search', { params })
        .then(response => {
          return axios.get(`http://localhost:5000/users/${this.userId}/favorites`).then(favoritesResponse => {
            const favoriteIds = new Set(favoritesResponse.data.map(fav => fav.id));
            this.projects = response.data.map(project => ({
              ...project,
              isFavorited: favoriteIds.has(project.id) // 根据用户的收藏状态设置 isFavorited
            }));
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
      if (project.isFavorited) {
        axios.post('http://localhost:5000/projects/unfavorite', {
          user_id: this.userId,
          project_id: project.id
        })
        .then(() => {
          project.isFavorited = false;
        })
        .catch(error => {
          console.error("取消收藏时出错: ", error);
        });
      } else {
        axios.post('http://localhost:5000/projects/favorite', {
          user_id: this.userId,
          project_id: project.id
        })
        .then(() => {
          project.isFavorited = true;
        })
        .catch(error => {
          console.error("收藏项目时出错: ", error);
        });
      }
    },
    joinProject(projectId) {
      axios.post(`http://localhost:5000/projects/${projectId}/participate`, {}, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}` // 使用 JWT 进行认证
        }
      })
      .then(response => {
        this.message = response.data.message; // 显示成功消息
      })
      .catch(error => {
        console.error("加入项目时出错: ", error);
        this.message = error.response ? error.response.data.message : "网络错误"; // 显示错误消息
      });
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
      this.userId = decodedToken.sub;  // 假设 sub 包含用户ID
    }

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
}

.search-button {
  padding: 10px 20px;
  background-color: #3498db;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.search-button:hover {
  background-color: #2980b9;
}

.projects-list {
  list-style: none;
  padding: 0;
}

.project-card {
  padding: 20px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  position: relative; /* 为创建者信息定位做准备 */
}

.project-title {
  font-size: 24px;
  color: #2c3e50;
  margin: 0 0 10px;
}

.project-content {
  font-size: 16px;
  color: #34495e;
}

.button-container {
  display: flex;
  gap: 10px;
  margin-top: 10px; /* 与其他内容保持间距 */
}

.project-type,
.professional-type {
  padding: 8px 15px; /* 增加标签大小 */
  border-radius: 8px;
  background-color: rgba(236, 240, 241, 0.8); /* 半透明背景色 */
  cursor: pointer;
  transition: background-color 0.3s, box-shadow 0.3s;
  font-size: 14px; /* 标签字体稍大 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.project-type:hover,
.professional-type:hover {
  background-color: rgba(189, 195, 199, 0.8); /* 悬停时背景稍深 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 增加阴影 */
}

.project-created-by {
  font-size: 14px;
  color: #7f8c8d;
  position: absolute;
  top: 10px;
  left: 20px;
}

.favorite-button {
  padding: 5px 10px; /* 缩小按钮 */
  border: none;
  border-radius: 5px;
  cursor: pointer;
  background-color: #b2bec3; /* 柔和的灰色 */
  color: #2d3436;
  transition: background-color 0.3s, transform 0.2s ease;
  font-size: 14px; /* 字体稍小 */
  margin-top: 10px; /* 调整按钮与其他内容的间距 */
}

.favorite-button:hover {
  background-color: #636e72;
  transform: translateY(-2px);
}

.favorited {
  background-color: #d63031; /* 收藏状态下的背景颜色 */
  color: #fff; /* 收藏状态下文字颜色 */
}

.message {
  margin-top: 10px;
  color: #2c3e50; /* 或其他你喜欢的颜色 */
  font-weight: bold; /* 或者其他样式 */
}
</style>


