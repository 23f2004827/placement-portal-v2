<template>
  <div class="register-container">
    <div class="card shadow p-4" style="max-width: 500px; width: 100%; margin: 50px auto;">
      <h2 class="text-center mb-4 text-primary">Student Registration</h2>
      <form @submit.prevent="handleRegister">
        <div class="mb-3">
          <label class="form-label">Full Name</label>
          <input type="text" class="form-control" v-model="form.full_name" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Email address</label>
          <input type="email" class="form-control" v-model="form.email" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" class="form-control" v-model="form.password" required>
        </div>
        <button type="submit" class="btn btn-primary w-100">Register</button>
      </form>
      <div class="text-center mt-3">
        <router-link to="/login">Already have an account? Login</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return { form: { full_name: '', email: '', password: '' } }
  },
  methods: {
    async handleRegister() {
      try {
        await axios.post('/api/register/student', this.form);
        alert('Registration successful! You can now login.');
        this.$router.push('/login');
      } catch (err) {
        alert(err.response?.data?.message || 'Registration failed');
      }
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f8f9fa;
}
</style>
