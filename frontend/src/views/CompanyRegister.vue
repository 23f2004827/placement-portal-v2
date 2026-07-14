<template>
  <div class="register-container py-5">
    <div class="card shadow p-4" style="max-width: 600px; width: 100%; margin: 0 auto;">
      <h2 class="text-center mb-4 text-primary">Company Registration</h2>
      <form @submit.prevent="handleRegister">
        <div class="mb-3">
          <label class="form-label">Company Name</label>
          <input type="text" class="form-control" v-model="form.company_name" required>
        </div>
        <div class="mb-3">
          <label class="form-label">HR Contact Name</label>
          <input type="text" class="form-control" v-model="form.full_name" required>
        </div>
        <div class="mb-3">
          <label class="form-label">HR Email address (Login ID)</label>
          <input type="email" class="form-control" v-model="form.email" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input type="password" class="form-control" v-model="form.password" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Contact Number (Optional)</label>
          <input type="text" class="form-control" v-model="form.hr_contact">
        </div>
        <div class="mb-3">
          <label class="form-label">Company Website</label>
          <input type="url" class="form-control" v-model="form.website" placeholder="https://">
        </div>
        <button type="submit" class="btn btn-primary w-100">Register Company</button>
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
    return { form: { company_name: '', full_name: '', email: '', password: '', hr_contact: '', website: '' } }
  },
  methods: {
    async handleRegister() {
      try {
        await axios.post('/api/register/company', this.form);
        alert('Registration successful! Awaiting admin approval before you can create drives.');
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
