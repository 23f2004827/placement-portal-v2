<template>
  <div class="login-container">
    <div class="card shadow p-4" style="max-width: 400px; width: 100%; margin: 50px auto;">
      <h2 class="text-center mb-4 text-primary">Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label class="form-label">Email address</label>
          <input type="email" class="form-control" v-model="email" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" class="form-control" v-model="password" required>
        </div>
        <button type="submit" class="btn btn-primary w-100">Login</button>
      </form>
      <div class="text-center mt-3">
        <p>Don't have an account?</p>
        <router-link to="/register">Register as Student</router-link> | 
        <router-link to="/register-company">Register as Company</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'UserLogin',
  data() {
    return { email: '', password: '' }
  },
  methods: {
    async handleLogin() {
      try {
        const res = await axios.post('/api/login', { email: this.email, password: this.password });
        if(res.status === 200) {
          localStorage.setItem('token', 'dummy-token'); // Simple token auth
          localStorage.setItem('role', res.data.user.role);
          if (res.data.user.role === 'admin') this.$router.push('/admin');
          else if (res.data.user.role === 'company') this.$router.push('/company');
          else this.$router.push('/student');
        }
      } catch (err) {
        alert(err.response?.data?.message || 'Login failed');
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f8f9fa;
}
</style>