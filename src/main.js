import { createApp } from 'vue'; // 使用 Vue 3 的 import 方式
import App from './App.vue';
import { createRouter, createWebHistory } from 'vue-router'; // 从 'vue-router' 导入 createRouter 和 createWebHistory
import UserRegister from './components/UserRegister.vue';
import UserLogin from './components/UserLogin.vue';
import CreateProject from './components/CreateProject.vue';
import ViewProjects from './components/ViewProjects.vue';
import Home from './components/HomePage.vue';
import ViewUsers from './components/ViewUsers.vue';
import ViewUserProfile from './components/ViewUserProfile.vue';
import EditUserProfile from './components/EditUserProfile.vue';
import Chat from './components/ChatMessage.vue'; // 导入聊天组件
import RecentChats from './components/RecentChats.vue'; // 导入最近聊天组件
import FavoriteProjects from './components/FavoriteProjects.vue';
import ViewMyProjects from './components/ViewMyProjects.vue';
import MyMessage from './components/MyMessage.vue';
import MyparticipateProjects from './components/MyparticipateProjects.vue';

// 定义路由
const routes = [
  { path: '/', component: Home },
  { path: '/register', component: UserRegister },
  { path: '/login', component: UserLogin },
  { path: '/create-project', component: CreateProject },
  { path: '/projects', component: ViewProjects },
  { path: '/users', component: ViewUsers } ,
  { path: '/user/:username', component: ViewUserProfile },  // 动态路由，支持查看不同用户信息
  { path: '/edit-profile', component: EditUserProfile } ,   // 编辑用户信息
  { path: '/chat/:recipientId', component: Chat } ,
  { path: '/recent-chats', component: RecentChats }, // 最近聊天的路由
  { path: '/favorites', component: FavoriteProjects }, // 新增收藏项目的路由
  { path: '/projects/my-projects', component: ViewMyProjects }, // 新增查看自己发布的项目的路由
  { path: '/messages', component: MyMessage},
  { path: '/my-participate-projects', component: MyparticipateProjects},
  
];

// 创建路由实例
const router = createRouter({
  history: createWebHistory(), // 使用 HTML5 history 模式
  routes
});

// 创建 Vue 应用
const app = createApp(App);

// 使用路由
app.use(router);

// 挂载应用
app.mount('#app');
