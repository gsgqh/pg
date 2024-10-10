<template>
  <!-- 背景容器 -->
  <div class="particles-background"></div>

  <div class="create-project-container">
    <h2 class="create-project-title">创建新项目</h2>
    <div class="form-container">
      <input
        v-model="projectTitle"
        @input="checkTitleLength"
        placeholder="项目标题 (最多 50 字符)"
        class="input-field"
      />
      <p class="char-count">{{ projectTitle.length }}/50</p>

      <textarea
        v-model="projectContent"
        @input="checkContentLength"
        placeholder="项目内容 (最多 2000 字符)"
        class="input-field textarea-field"
      ></textarea>
      <p class="char-count">{{ projectContent.length }}/2000</p>

      <select v-model="projectCategory" class="input-field select-category">
        <option disabled value="">请选择项目类别</option>
        <option>项目</option>
        <option>竞赛</option>
        <option>科研</option>
        <option>学习</option>
      </select>

      <select v-model="majorType" class="input-field select-major">
        <option disabled value="">请选择专业类型</option>
        <option>哲学</option>
        <option>经济学</option>
        <option>法学</option>
        <option>教育学</option>
        <option>文学</option>
        <option>历史学</option>
        <option>理学</option>
        <option>工学</option>
        <option>农学</option>
        <option>医学</option>
        <option>管理学</option>
        <option>艺术学</option>
      </select>

      <label for="file-upload" class="file-upload-label">选择照片</label>
      <input
        type="file"
        id="file-upload"
        @change="handleFileUpload"
        multiple
        accept="image/*"
        class="input-field file-input"
      />
      <p class="info-text">最多上传 9 张图片 (已选择 {{ selectedFiles.length }} 张)</p>

      <button @click="createProject" class="create-button" :disabled="isDisabled">创建项目</button>

      <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'CreateProject',
  data() {
    return {
      projectTitle: '',
      projectContent: '',
      projectCategory: '',
      majorType: '',
      successMessage: '',
      errorMessage: '',
      maxTitleLength: 50,
      maxContentLength: 500,
      selectedFiles: []  // 存储选中的文件
    };
  },
  computed: {
    isDisabled() {
      return (
        !this.projectTitle ||
        this.projectTitle.length > this.maxTitleLength ||
        !this.projectContent ||
        this.projectContent.length > this.maxContentLength ||
        !this.projectCategory ||
        !this.majorType ||
        (this.selectedFiles.length > 9)  // 限制图片数量
      );
    }
  },
  methods: {
    checkTitleLength() {
      if (this.projectTitle.length > this.maxTitleLength) {
        this.projectTitle = this.projectTitle.slice(0, this.maxTitleLength);
      }
    },
    checkContentLength() {
      if (this.projectContent.length > this.maxContentLength) {
        this.projectContent = this.projectContent.slice(0, this.maxContentLength);
      }
    },
    handleFileUpload(event) {
      this.selectedFiles = Array.from(event.target.files).slice(0, 9);  // 获取最多9张图片
    },
    createProject() {
      this.successMessage = '';
      this.errorMessage = '';

      const formData = new FormData();
      formData.append('title', this.projectTitle);
      formData.append('content', this.projectContent);
      formData.append('category', this.projectCategory);
      formData.append('major_type', this.majorType);
      this.selectedFiles.forEach(file => {
        formData.append('images', file);
      });

      axios.post('http://localhost:5000/create-project', formData, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        if (response.data.success) {
          this.successMessage = response.data.message;
          setTimeout(() => {
            this.$router.push('/projects');
          }, 1500);
        } else {
          this.errorMessage = response.data.message;
        }
      })
      .catch(error => {
        if (error.response) {
          this.errorMessage = error.response.data.message;
        } else {
          this.errorMessage = 'An error occurred while creating the project.';
        }
      });
    }
  }
};
</script>


<style scoped>
/* 粒子背景样式 */
.particles-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(-45deg, #1e3c72, #2a5298, #e8f5e9, #ffffff);
  background-size: 400% 400%;
  animation: gradientAnimation 15s ease infinite;
  z-index: -1; /* 确保背景在所有内容的后面 */
}

@keyframes gradientAnimation {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.create-project-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
  position: relative;
  z-index: 1; /* 确保内容在背景上方 */
}

.create-project-title {
  text-align: center;
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 30px;
  border-bottom: 2px solid #3498db;
  padding-bottom: 10px;
}

.form-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-field {
  width: calc(100% - 40px);
  padding: 14px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-sizing: border-box;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  margin: 0 20px;
}

.input-field:focus {
  border-color: #3498db;
  box-shadow: 0 0 8px rgba(52, 152, 219, 0.3);
  outline: none;
}

.textarea-field {
  height: 150px;
  resize: vertical;
}

.select-category, .select-major {
  background-color: #f4f4f4;
}

.file-upload-label {
  width: 200px;
  padding: 10px;
  background-color: #42b983;
  color: #fff;
  text-align: center;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  margin: 0 auto;
  font-size: 16px;
  font-weight: bold;
}

.file-upload-label:hover {
  background-color: #3ca772;
  transform: translateY(-3px);
}

.file-input {
  display: none;
}

.create-button {
  width: calc(100% - 40px);
  padding: 14px;
  font-size: 16px;
  color: #fff;
  background-color: #3498db;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  margin: 0 20px;
}

.create-button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.create-button:hover:enabled {
  background-color: #2980b9;
  transform: translateY(-3px);
}

.create-button:active:enabled {
  background-color: #1c6380;
  transform: translateY(0);
}

.char-count {
  font-size: 12px;
  color: #888;
  text-align: right;
  margin-right: 20px;
  font-style: italic;
}

.success-message, .error-message {
  font-size: 14px;
  margin-top: 10px;
  text-align: center;
  padding: 10px;
  border-radius: 5px;
  max-width: 90%;
  margin-left: auto;
  margin-right: auto;
}

.success-message {
  background-color: #e0f8e0;
  color: #28a745;
}

.error-message {
  background-color: #f8e0e0;
  color: #dc3545;
}

.info-text {
  font-size: 14px;
  color: #888;
  text-align: center;
  margin-top: -10px;
  margin-bottom: 20px;
  font-style: italic;
}
</style>