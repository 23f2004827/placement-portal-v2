<template>
  <div class="home-container">
    <div class="hero-section text-center p-5 rounded-3 shadow-lg bg-light text-dark mx-auto" style="max-width: 800px; margin-top: 50px;">
      <h1 class="display-4 fw-bold">Welcome to Placement Portal</h1>
      <p class="lead mt-3 text-muted">Your ultimate platform for campus placements and recruitment.</p>
      <div class="mt-4">
        <router-link to="/login" class="btn btn-primary btn-lg m-2">Login</router-link>
        <router-link to="/register" class="btn btn-outline-success btn-lg m-2">Student Register</router-link>
        <router-link to="/register-company" class="btn btn-outline-info btn-lg m-2">Company Register</router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage'
};
</script>

<style scoped>
.container {
  margin-top: 5rem;
}
</style> 