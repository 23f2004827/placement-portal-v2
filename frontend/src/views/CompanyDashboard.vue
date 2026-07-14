<template>
  <div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Company Dashboard</h2>
      <button class="btn btn-outline-danger" @click="logout">Logout</button>
    </div>

    <div v-if="!profile.is_approved" class="alert alert-warning mb-4">
      Your company registration is currently pending admin approval. You cannot create placement drives yet.
    </div>

    <!-- Tabs -->
    <ul class="nav nav-tabs mb-4">
      <li class="nav-item">
        <a class="nav-link" :class="{active: activeTab === 'profile'}" href="#" @click.prevent="activeTab = 'profile'">Company Profile</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{active: activeTab === 'create_drive'}" href="#" @click.prevent="activeTab = 'create_drive'">Create Drive</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{active: activeTab === 'my_drives'}" href="#" @click.prevent="activeTab = 'my_drives'">My Drives</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{active: activeTab === 'applications'}" href="#" @click.prevent="activeTab = 'applications'">Student Applications</a>
      </li>
    </ul>

    <!-- Profile Tab -->
    <div v-if="activeTab === 'profile'" class="card shadow-sm p-4" style="max-width: 600px;">
      <h4 class="mb-4">Update Profile</h4>
      <form @submit.prevent="updateProfile">
        <div class="mb-3">
          <label class="form-label">Company Name</label>
          <input type="text" class="form-control" v-model="profileForm.company_name" required>
        </div>
        <div class="mb-3">
          <label class="form-label">HR Contact Name</label>
          <input type="text" class="form-control" v-model="profileForm.hr_contact">
        </div>
        <div class="mb-3">
          <label class="form-label">Website</label>
          <input type="url" class="form-control" v-model="profileForm.website">
        </div>
        <button type="submit" class="btn btn-primary">Save Profile</button>
      </form>
    </div>

    <!-- Create Drive Tab -->
    <div v-if="activeTab === 'create_drive'">
      <div v-if="profile.is_approved" class="card shadow-sm p-4 mb-5" style="max-width: 800px;">
        <h4 class="mb-3">Create New Placement Drive</h4>
        <form @submit.prevent="createDrive">
          <div class="mb-3">
            <label class="form-label">Job Title</label>
            <input type="text" class="form-control" v-model="driveForm.job_title" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Job Description</label>
            <textarea class="form-control" v-model="driveForm.job_description" rows="3" required></textarea>
          </div>
          <div class="row">
            <div class="col-md-4 mb-3">
              <label class="form-label">Eligible Branches</label>
              <input type="text" class="form-control" v-model="driveForm.eligible_branches" placeholder="e.g. CSE, ECE">
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label">Min CGPA</label>
              <input type="number" step="0.1" class="form-control" v-model="driveForm.min_cgpa">
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label">Eligible Years</label>
              <input type="text" class="form-control" v-model="driveForm.eligible_years" placeholder="e.g. 2024, 2025">
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label">Application Deadline</label>
            <input type="datetime-local" class="form-control" v-model="driveForm.application_deadline" required>
          </div>
          <button type="submit" class="btn btn-success">Create Drive</button>
        </form>
      </div>
    </div>
      
    <!-- My Drives Tab -->
    <div v-if="activeTab === 'my_drives'">
      <h4>My Created Drives</h4>
      <table class="table table-hover table-bordered bg-white shadow-sm mt-3">
        <thead class="table-light">
          <tr>
            <th>Job Title</th>
            <th>Description</th>
            <th>Deadline</th>
            <th>Status</th>
            <th>Applicants</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="drive in drives" :key="drive.id">
            <td>{{ drive.job_title }}</td>
            <td>{{ drive.job_description }}</td>
            <td>{{ new Date(drive.deadline).toLocaleString() }}</td>
            <td>
              <span class="badge" :class="drive.status === 'Approved' ? 'bg-success' : 'bg-warning'">
                {{ drive.status }}
              </span>
            </td>
            <td><strong>{{ drive.applicant_count }}</strong> applicants</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Applications Tab -->
    <div v-if="activeTab === 'applications'">
      <div class="row">
        <div class="col-md-3 border-end">
          <h5>Select a Drive</h5>
          <div class="list-group">
            <a href="#" v-for="drive in drives" :key="drive.id" 
               class="list-group-item list-group-item-action" 
               :class="{active: selectedDriveId === drive.id}"
               @click.prevent="selectDrive(drive.id)">
              {{ drive.job_title }}
            </a>
          </div>
        </div>
        <div class="col-md-9">
          <h5 v-if="!selectedDriveId">Select a drive to view student applications</h5>
          <div v-else>
            <h5>Applications for Selected Drive</h5>
            <table class="table table-hover bg-white shadow-sm mt-3">
              <thead class="table-light">
                <tr>
                  <th>Student Name</th>
                  <th>Email</th>
                  <th>Branch</th>
                  <th>CGPA</th>
                  <th>Applied On</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="app in applications" :key="app.application_id">
                  <td>{{ app.student_name }}</td>
                  <td>{{ app.student_email }}</td>
                  <td>{{ app.branch || 'N/A' }}</td>
                  <td>{{ app.cgpa || 'N/A' }}</td>
                  <td>{{ new Date(app.application_date).toLocaleDateString() }}</td>
                  <td>
                    <span class="badge bg-primary">{{ app.status }}</span>
                  </td>
                  <td>
                    <select class="form-select form-select-sm" @change="updateAppStatus(app.application_id, $event.target.value)">
                      <option value="" disabled selected>Update Status...</option>
                      <option value="Shortlisted">Shortlist</option>
                      <option value="Selected">Select</option>
                      <option value="Rejected">Reject</option>
                    </select>
                  </td>
                </tr>
                <tr v-if="applications.length === 0">
                  <td colspan="7" class="text-center text-muted">No applications found for this drive.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
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
      profileForm: { company_name: '', hr_contact: '', website: '' },
      drives: [],
      driveForm: { job_title: '', job_description: '', eligible_branches: '', min_cgpa: '', eligible_years: '', application_deadline: '' },
      selectedDriveId: null,
      applications: []
    }
  },
  async mounted() {
    this.fetchProfile();
    this.fetchDrives();
  },
  methods: {
    async fetchProfile() {
      try {
        const res = await axios.get('/api/company/profile');
        this.profile = res.data;
        this.profileForm = { ...res.data };
      } catch(err) { console.error(err); }
    },
    async updateProfile() {
      try {
        await axios.put('/api/company/profile', this.profileForm);
        alert('Profile updated successfully!');
        this.fetchProfile();
      } catch(err) { alert('Failed to update profile'); }
    },
    async fetchDrives() {
      try {
        const res = await axios.get('/api/company/drives');
        this.drives = res.data;
      } catch(err) { console.error(err); }
    },
    async createDrive() {
      try {
        // Convert local datetime to UTC ISO string format
        let payload = { ...this.driveForm };
        if (payload.application_deadline) {
          payload.application_deadline = new Date(payload.application_deadline).toISOString();
        }
        await axios.post('/api/company/drives', payload);
        alert('Drive created successfully! Awaiting admin approval.');
        this.driveForm = { job_title: '', job_description: '', eligible_branches: '', min_cgpa: '', eligible_years: '', application_deadline: '' };
        this.fetchDrives();
      } catch(err) {
        alert(err.response?.data?.message || 'Failed to create drive');
      }
    },
    async selectDrive(driveId) {
      this.selectedDriveId = driveId;
      try {
        const res = await axios.get(`/api/company/drives/${driveId}/applications`);
        this.applications = res.data;
      } catch(err) { console.error(err); }
    },
    async updateAppStatus(appId, status) {
      if(!status) return;
      try {
        await axios.put(`/api/company/applications/${appId}/status`, { status });
        alert(`Status updated to ${status}`);
        this.selectDrive(this.selectedDriveId); // Refresh
      } catch(err) {
        alert('Failed to update status');
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
