<template>
  <div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Student Dashboard</h2>
      <button class="btn btn-outline-danger" @click="logout">Logout</button>
    </div>

    <!-- Tabs -->
    <ul class="nav nav-tabs mb-4">
      <li class="nav-item">
        <a class="nav-link" :class="{active: activeTab === 'profile'}" href="#" @click.prevent="activeTab = 'profile'">My Profile</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{active: activeTab === 'drives'}" href="#" @click.prevent="activeTab = 'drives'">Browse Drives</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{active: activeTab === 'history'}" href="#" @click.prevent="activeTab = 'history'">Application History</a>
      </li>
    </ul>

    <!-- Profile Tab -->
    <div v-if="activeTab === 'profile'" class="card shadow-sm p-4" style="max-width: 600px;">
      <h4 class="mb-4">Update Student Profile</h4>
      <form @submit.prevent="updateProfile">
        <div class="mb-3">
          <label class="form-label">Full Name</label>
          <input type="text" class="form-control" v-model="profileForm.full_name" required>
        </div>
        <div class="mb-3">
          <label class="form-label">Branch</label>
          <input type="text" class="form-control" v-model="profileForm.branch" placeholder="e.g. CSE">
        </div>
        <div class="mb-3">
          <label class="form-label">CGPA</label>
          <input type="number" step="0.01" class="form-control" v-model="profileForm.cgpa" placeholder="e.g. 8.5">
        </div>
        <div class="mb-3">
          <label class="form-label">Graduation Year</label>
          <input type="number" class="form-control" v-model="profileForm.graduation_year" placeholder="e.g. 2025">
        </div>
        <div class="mb-3">
          <label class="form-label">Resume Link (Google Drive / GitHub)</label>
          <input type="url" class="form-control" v-model="profileForm.resume_path" placeholder="https://...">
        </div>
        <button type="submit" class="btn btn-primary">Save Profile</button>
      </form>
    </div>

    <!-- Browse Drives Tab -->
    <div v-if="activeTab === 'drives'">
      <div class="mb-4 d-flex">
        <input type="text" class="form-control me-2" v-model="searchQuery" placeholder="Search by Job Title or Company..." style="max-width: 400px;">
        <div class="form-check d-flex align-items-center ms-3">
          <input class="form-check-input me-2" type="checkbox" v-model="filterEligible" id="eligibilityCheck">
          <label class="form-check-label" for="eligibilityCheck">Show Only Eligible Drives</label>
        </div>
      </div>
      
      <div class="row">
        <div class="col-md-4 mb-4" v-for="drive in filteredDrives" :key="drive.id">
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <h5 class="card-title text-primary">{{ drive.job_title }}</h5>
              <h6 class="card-subtitle mb-3 text-muted">{{ drive.company_name }}</h6>
              <p class="card-text small">{{ drive.job_description.substring(0, 100) }}...</p>
              
              <hr>
              <p class="mb-1 small"><strong>Eligibility:</strong> {{ drive.eligible_branches || 'Any' }} | CGPA {{ drive.min_cgpa }}+ | {{ drive.eligible_years || 'Any Year' }}</p>
              <p class="mb-3 small text-danger"><strong>Deadline:</strong> {{ new Date(drive.deadline).toLocaleString() }}</p>
              
              <button class="btn btn-success w-100" @click="applyForDrive(drive.id)">Apply Now</button>
            </div>
          </div>
        </div>
        <div v-if="filteredDrives.length === 0" class="col-12 text-center mt-5 text-muted">
          <h5>No placement drives found matching your criteria.</h5>
        </div>
      </div>
    </div>

    <!-- Application History Tab -->
    <div v-if="activeTab === 'history'">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h4>My Applications</h4>
        <button class="btn btn-outline-success" @click="exportCSV">
          <i class="fas fa-download me-2"></i> Export to CSV
        </button>
      </div>
      <table class="table table-hover table-bordered bg-white shadow-sm mt-3">
        <thead class="table-light">
          <tr>
            <th>Company</th>
            <th>Job Title</th>
            <th>Applied On</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in applications" :key="app.application_id">
            <td>{{ app.company_name }}</td>
            <td>{{ app.job_title }}</td>
            <td>{{ new Date(app.application_date).toLocaleString() }}</td>
            <td>
              <span class="badge" 
                    :class="{
                      'bg-primary': app.status === 'Applied',
                      'bg-warning text-dark': app.status === 'Shortlisted',
                      'bg-success': app.status === 'Selected',
                      'bg-danger': app.status === 'Rejected'
                    }">
                {{ app.status }}
              </span>
            </td>
          </tr>
          <tr v-if="applications.length === 0">
            <td colspan="4" class="text-center text-muted">You haven't applied to any drives yet.</td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      activeTab: 'profile',
      profile: {},
      profileForm: { full_name: '', branch: '', cgpa: '', graduation_year: '', resume_path: '' },
      drives: [],
      applications: [],
      searchQuery: '',
      filterEligible: false
    }
  },
  computed: {
    filteredDrives() {
      return this.drives.filter(d => {
        // Search Filter
        const query = this.searchQuery.toLowerCase();
        const matchesSearch = d.job_title.toLowerCase().includes(query) || d.company_name.toLowerCase().includes(query);
        
        // Eligibility Filter
        let isEligible = true;
        if(this.filterEligible) {
          const p = this.profile;
          if(d.min_cgpa && p.cgpa < d.min_cgpa) isEligible = false;
          if(d.eligible_branches && p.branch && !d.eligible_branches.toLowerCase().includes(p.branch.toLowerCase())) isEligible = false;
          if(d.eligible_years && p.graduation_year && !d.eligible_years.includes(p.graduation_year.toString())) isEligible = false;
        }

        return matchesSearch && isEligible;
      });
    }
  },
  async mounted() {
    this.fetchData();
  },
  watch: {
    activeTab() {
      this.fetchData();
    }
  },
  methods: {
    async fetchData() {
      try {
        if(this.activeTab === 'profile') {
          const res = await axios.get('/api/student/profile');
          this.profile = res.data;
          this.profileForm = { ...res.data };
        } else if(this.activeTab === 'drives') {
          const res = await axios.get('/api/student/drives');
          this.drives = res.data;
        } else if(this.activeTab === 'history') {
          const res = await axios.get('/api/student/applications');
          this.applications = res.data;
        }
      } catch(err) { console.error(err); }
    },
    async updateProfile() {
      try {
        await axios.put('/api/student/profile', this.profileForm);
        alert('Profile updated successfully!');
        this.fetchData();
      } catch(err) { alert('Failed to update profile'); }
    },
    async applyForDrive(driveId) {
      if(!confirm("Are you sure you want to apply for this drive?")) return;
      try {
        await axios.post(`/api/student/drives/${driveId}/apply`);
        alert('Application successful!');
        this.activeTab = 'history'; // Switch to history tab to view it
      } catch(err) {
        alert(err.response?.data?.message || 'Application failed');
      }
    },
    async exportCSV() {
      try {
        const res = await axios.post('/api/student/export');
        alert(res.data.message);
      } catch (err) {
        alert('Export failed');
      }
    },
    async logout() {
      await axios.post('/api/logout');
      localStorage.clear();
      this.$router.push('/login');
    }
  }
}
</script>
