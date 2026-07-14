<template>
  <div class="container-fluid mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Admin Dashboard</h2>
      <button class="btn btn-outline-danger" @click="logout">Logout</button>
    </div>

    <!-- Tabs -->
    <ul class="nav nav-tabs mb-4">
      <li class="nav-item">
        <a class="nav-link" :class="{active: activeTab === 'stats'}" href="#" @click.prevent="activeTab = 'stats'">Overview</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{active: activeTab === 'companies'}" href="#" @click.prevent="activeTab = 'companies'">Companies</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{active: activeTab === 'students'}" href="#" @click.prevent="activeTab = 'students'">Students</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{active: activeTab === 'drives'}" href="#" @click.prevent="activeTab = 'drives'">Placement Drives</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" :class="{active: activeTab === 'applications'}" href="#" @click.prevent="activeTab = 'applications'">Applications</a>
      </li>
    </ul>

    <!-- Stats Tab -->
    <div v-if="activeTab === 'stats'">
      <div class="row">
        <div class="col-md-4">
          <div class="card text-white bg-primary mb-3 shadow">
            <div class="card-body">
              <h5 class="card-title">Total Students</h5>
              <p class="card-text display-4">{{ stats.total_students }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-success mb-3 shadow">
            <div class="card-body">
              <h5 class="card-title">Total Companies</h5>
              <p class="card-text display-4">{{ stats.total_companies }}</p>
            </div>
          </div>
        </div>
        <div class="col-md-4">
          <div class="card text-white bg-info mb-3 shadow">
            <div class="card-body">
              <h5 class="card-title">Total Drives</h5>
              <p class="card-text display-4">{{ stats.total_drives }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Companies Tab -->
    <div v-if="activeTab === 'companies'">
      <div class="mb-3">
        <input type="text" class="form-control" v-model="companySearch" placeholder="Search companies by name or email...">
      </div>
      <table class="table table-hover table-bordered bg-white shadow-sm">
        <thead class="table-light">
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>HR Contact</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="comp in filteredCompanies" :key="comp.id">
            <td>{{ comp.company_name }}</td>
            <td>{{ comp.email }}</td>
            <td>{{ comp.hr_contact }}</td>
            <td>
              <span class="badge" :class="comp.is_approved ? 'bg-success' : 'bg-warning'">
                {{ comp.is_approved ? 'Approved' : 'Pending' }}
              </span>
              <span class="badge ms-1" :class="comp.is_active ? 'bg-info' : 'bg-danger'">
                {{ comp.is_active ? 'Active' : 'Blacklisted' }}
              </span>
            </td>
            <td>
              <button v-if="!comp.is_approved" class="btn btn-sm btn-success me-1" @click="updateCompany(comp.id, 'approve')">Approve</button>
              <button v-if="comp.is_approved" class="btn btn-sm btn-outline-warning me-1" @click="updateCompany(comp.id, 'reject')">Reject</button>
              <button v-if="comp.is_active" class="btn btn-sm btn-danger" @click="updateCompany(comp.id, 'blacklist')">Blacklist</button>
              <button v-else class="btn btn-sm btn-secondary" @click="updateCompany(comp.id, 'activate')">Activate</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Students Tab -->
    <div v-if="activeTab === 'students'">
      <div class="mb-3">
        <input type="text" class="form-control" v-model="studentSearch" placeholder="Search students by name or email...">
      </div>
      <table class="table table-hover table-bordered bg-white shadow-sm">
        <thead class="table-light">
          <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Branch</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="student in filteredStudents" :key="student.id">
            <td>{{ student.full_name }}</td>
            <td>{{ student.email }}</td>
            <td>{{ student.branch || 'N/A' }}</td>
            <td>
              <span class="badge" :class="student.is_active ? 'bg-success' : 'bg-danger'">
                {{ student.is_active ? 'Active' : 'Blacklisted' }}
              </span>
            </td>
            <td>
              <button v-if="student.is_active" class="btn btn-sm btn-danger" @click="updateStudent(student.id, 'blacklist')">Blacklist</button>
              <button v-else class="btn btn-sm btn-secondary" @click="updateStudent(student.id, 'activate')">Activate</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Drives Tab -->
    <div v-if="activeTab === 'drives'">
      <table class="table table-hover table-bordered bg-white shadow-sm">
        <thead class="table-light">
          <tr>
            <th>Company</th>
            <th>Job Title</th>
            <th>Deadline</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="drive in drives" :key="drive.id">
            <td>{{ drive.company_name }}</td>
            <td>{{ drive.job_title }}</td>
            <td>{{ new Date(drive.deadline).toLocaleDateString() }}</td>
            <td>
              <span class="badge" :class="drive.status === 'Approved' ? 'bg-success' : (drive.status === 'Pending' ? 'bg-warning' : 'bg-secondary')">
                {{ drive.status }}
              </span>
            </td>
            <td>
              <button v-if="drive.status === 'Pending'" class="btn btn-sm btn-success me-1" @click="updateDrive(drive.id, 'Approved')">Approve</button>
              <button v-if="drive.status === 'Pending'" class="btn btn-sm btn-danger me-1" @click="updateDrive(drive.id, 'Closed')">Reject</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Applications Tab -->
    <div v-if="activeTab === 'applications'">
      <table class="table table-hover table-bordered bg-white shadow-sm">
        <thead class="table-light">
          <tr>
            <th>Student</th>
            <th>Company</th>
            <th>Job Title</th>
            <th>Applied On</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="app in applications" :key="app.id">
            <td>{{ app.student_name }}</td>
            <td>{{ app.company_name }}</td>
            <td>{{ app.job_title }}</td>
            <td>{{ new Date(app.application_date).toLocaleDateString() }}</td>
            <td>
              <span class="badge bg-primary">
                {{ app.status }}
              </span>
            </td>
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
      activeTab: 'stats',
      stats: { total_students: 0, total_companies: 0, total_drives: 0 },
      companies: [],
      students: [],
      drives: [],
      applications: [],
      companySearch: '',
      studentSearch: ''
    }
  },
  computed: {
    filteredCompanies() {
      if(!this.companySearch) return this.companies;
      const s = this.companySearch.toLowerCase();
      return this.companies.filter(c => 
        (c.company_name && c.company_name.toLowerCase().includes(s)) || 
        c.email.toLowerCase().includes(s)
      );
    },
    filteredStudents() {
      if(!this.studentSearch) return this.students;
      const s = this.studentSearch.toLowerCase();
      return this.students.filter(st => 
        st.full_name.toLowerCase().includes(s) || 
        st.email.toLowerCase().includes(s)
      );
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
        if(this.activeTab === 'stats') {
          const res = await axios.get('/api/admin/stats');
          this.stats = res.data;
        } else if(this.activeTab === 'companies') {
          const res = await axios.get('/api/admin/companies');
          this.companies = res.data;
        } else if(this.activeTab === 'students') {
          const res = await axios.get('/api/admin/students');
          this.students = res.data;
        } else if(this.activeTab === 'drives') {
          const res = await axios.get('/api/admin/drives');
          this.drives = res.data;
        } else if(this.activeTab === 'applications') {
          const res = await axios.get('/api/admin/applications');
          this.applications = res.data;
        }
      } catch(err) {
        console.error("Failed to fetch data", err);
      }
    },
    async updateCompany(id, action) {
      if(confirm(`Are you sure you want to ${action} this company?`)) {
        await axios.put(`/api/admin/companies/${id}/status`, { action });
        this.fetchData();
      }
    },
    async updateStudent(id, action) {
      if(confirm(`Are you sure you want to ${action} this student?`)) {
        await axios.put(`/api/admin/students/${id}/status`, { action });
        this.fetchData();
      }
    },
    async updateDrive(id, status) {
      if(confirm(`Update drive status to ${status}?`)) {
        await axios.put(`/api/admin/drives/${id}/status`, { status });
        this.fetchData();
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