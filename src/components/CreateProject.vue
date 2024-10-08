<template>
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
        placeholder="项目内容 (最多 500 字符)"
        class="input-field textarea-field"
      ></textarea>
      <p class="char-count">{{ projectContent.length }}/500</p>

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
      maxTitleLength: 50,   // 最大标题长度
      maxContentLength: 500 // 最大内容长度
    };
  },
  computed: {
    isDisabled() {
      // 如果任一输入框为空或超出字符限制，则禁用按钮
      return (
        !this.projectTitle ||
        this.projectTitle.length > this.maxTitleLength ||
        !this.projectContent ||
        this.projectContent.length > this.maxContentLength ||
        !this.projectCategory ||
        !this.majorType
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
    createProject() {
      this.successMessage = '';
      this.errorMessage = '';

      axios.post('http://localhost:5000/create-project', {
        title: this.projectTitle,
        content: this.projectContent,
        category: this.projectCategory,
        major_type: this.majorType
      }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
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
.create-project-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
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
</style>
