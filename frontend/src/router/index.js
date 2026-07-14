import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../views/Home.vue';
import UserLogin from '../views/Login.vue';
import StudentRegister from '../views/StudentRegister.vue';
import CompanyRegister from '../views/CompanyRegister.vue';
import StudentDashboard from '../views/StudentDashboard.vue';
import CompanyDashboard from '../views/CompanyDashboard.vue';
import AdminDashboard from '../views/AdminDashboard.vue';

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/login', name: 'Login', component: UserLogin, meta:{guest:true} },
  { path: '/register', name: 'StudentRegister', component: StudentRegister, meta:{guest:true} },
  { path: '/register-company', name: 'CompanyRegister', component: CompanyRegister, meta:{guest:true} },
  { path: '/student', name: 'StudentDashboard', component: StudentDashboard, meta:{requiresAuth:true, role:'student'} },
  { path: '/company', name: 'CompanyDashboard', component: CompanyDashboard, meta:{requiresAuth:true, role:'company'} },
  { path: '/admin', name: 'AdminDashboard', component: AdminDashboard, meta:{requiresAuth:true, role:'admin'} },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');
  
  if (to.meta.requiresAuth && !token) {
    return next('/login');
  }
  
  if (to.meta.role && to.meta.role !== role) {
    if (role === 'admin') return next('/admin');
    if (role === 'company') return next('/company');
    if (role === 'student') return next('/student');
    return next('/login');
  }

  if (to.meta.guest && token) {
    if (role === 'admin') return next('/admin');
    if (role === 'company') return next('/company');
    if (role === 'student') return next('/student');
  }
  
  if (to.path === '/' && token) {
    if (role === 'admin') return next('/admin');
    if (role === 'company') return next('/company');
    if (role === 'student') return next('/student');
  }
  
  next();
});

export default router;