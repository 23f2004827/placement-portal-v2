# Placement Portal V2

A full-stack web application that simplifies campus placement management by connecting students, companies, and administrators through a centralized platform. Students can explore placement drives and apply for jobs, companies can manage recruitment drives and applications, and administrators can manage users and approve placement activities.

## 1. Project Overview

Placement Portal V2 is developed using Flask for the backend and Vue.js for the frontend. The application exposes REST-style API endpoints and uses SQLAlchemy to manage relational data.

The project demonstrates full-stack application development, database management, authentication, role-based access, API integration, and background task processing.

## 2. Technology Stack

### Backend
- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-CORS
- Flask-Mail
- PyJWT (dependency included; token authentication requires completion)

### Frontend
- Vue.js 3
- Axios
- Vue Router
- Chart.js

### Database and Background Processing
- SQLite
- Celery
- Redis
- MailHog for local email testing

### Development Tools
- Git and GitHub
- npm
- Python virtual environments

## 3. Features

### Student
- Register and log in.
- View and update a student profile.
- Browse approved placement drives.
- Apply for placement opportunities.
- View submitted applications.
- Access the student dashboard.

### Company
- Register a company account.
- Maintain company profile information.
- Create and view placement drives.
- View applicants for placement drives.
- Update application statuses.
- Wait for administrator approval before publishing recruitment activities.

### Administrator
- View dashboard statistics.
- View registered students and companies.
- Approve, reject, activate, or deactivate company accounts.
- Manage student account status.
- View placement drives and update their approval status.
- View application records.

### Additional Capabilities
- REST-style API endpoints.
- SQLAlchemy-based database models.
- Vue.js frontend integrated with Axios.
- Cross-origin requests configured for local frontend development.
- Celery and Redis dependencies for background task processing.
- Email-related configuration using Flask-Mail.

## 4. Project Structure

```text
placement-portal-v2-main/
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── routes/
│   ├── api_auth.py
│   ├── admin.py
│   ├── company.py
│   └── student.py
├── tasks/
│   ├── celery_worker.py
│   └── email_tasks.py
└── frontend/
    ├── package.json
    ├── package-lock.json
    ├── vue.config.js
    └── src/
        ├── App.vue
        ├── api.js
        ├── main.js
        ├── router/
        └── views/
```

## 5. Prerequisites

Install the following software before running the application:

- Python 3.10 or 3.11
- Node.js and npm
- Git
- Redis, if using background jobs

Check your installations:

```bash
python --version
node --version
npm --version
git --version
```

On some systems, use `python3` instead of `python`.

## 6. Installation and Setup

### Step 1: Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd placement-portal-v2-main
```

Replace the placeholder with the URL of your public GitHub repository.

Alternatively, extract the project ZIP and open its main directory in a terminal.

### Step 2: Create a Python Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Activate it on macOS or Linux:

```bash
source venv/bin/activate
```

### Step 3: Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Set a secure Flask secret key before running the application.

Example for macOS or Linux:

```bash
export SECRET_KEY="replace-with-a-secure-random-secret"
```

Example for Windows PowerShell:

```powershell
$env:SECRET_KEY="replace-with-a-secure-random-secret"
```

The current application uses SQLite and is configured to connect to Redis at `redis://localhost:6379/0` for Celery.

Keep secrets out of source control. Do not commit passwords, credentials, or production secret keys.

### Step 5: Start the Backend

From the project root, run:

```bash
python app.py
```

The application initializes the database tables and starts the Flask development server.

The default backend address is:

```text
http://127.0.0.1:5000
```

The current development configuration creates an initial administrator account when the database is empty:

- Email: `admin@example.com`
- Password: `admin123`

**Security warning:** These are development credentials only. Change or replace the default administrator credentials before deploying or sharing a live application.

### Step 6: Install Frontend Dependencies

Open a second terminal and navigate to the frontend directory:

```bash
cd frontend
npm install
```

### Step 7: Start the Frontend

```bash
npm run serve
```

Open the local frontend URL printed in the terminal, normally:

```text
http://localhost:8080
```

Keep the backend and frontend terminals running while using the application.

## 7. API Documentation

The backend exposes endpoints under `/api`. Requests and responses generally use JSON.

### Authentication and Registration

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/register/student` | Register a student |
| POST | `/api/register/company` | Register a company |
| POST | `/api/login` | Log in |
| POST | `/api/logout` | Log out |
| GET | `/api/me` | Get the current user's details |

Example student registration request:

```json
{
  "email": "student@example.com",
  "password": "your-password",
  "full_name": "Example Student"
}
```

Example login request:

```json
{
  "email": "student@example.com",
  "password": "your-password"
}
```

Send JSON requests with the `Content-Type: application/json` header.

**Authentication note:** The current login implementation uses Flask-Login sessions. Although PyJWT is listed as a dependency, the login endpoint does not currently issue a JWT access token. Protected endpoints therefore depend on the session-based authentication mechanism.

### Student Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/student/profile` | Retrieve student profile |
| PUT | `/api/student/profile` | Update student profile |
| GET | `/api/student/drives` | List approved placement drives |
| POST | `/api/student/drives/<drive_id>/apply` | Apply to a placement drive |
| GET | `/api/student/applications` | View submitted applications |
| POST | `/api/student/export` | Request student data export |

### Company Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/company/profile` | Retrieve company profile |
| PUT | `/api/company/profile` | Update company profile |
| GET | `/api/company/drives` | List the company's placement drives |
| POST | `/api/company/drives` | Create a placement drive |
| GET | `/api/company/drives/<drive_id>/applications` | View applicants for a drive |
| PUT | `/api/company/applications/<app_id>/status` | Update an application status |

### Administrator Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/admin/stats` | Retrieve dashboard statistics |
| GET | `/api/admin/companies` | List companies |
| PUT | `/api/admin/companies/<user_id>/status` | Update company status |
| GET | `/api/admin/students` | List students |
| PUT | `/api/admin/students/<user_id>/status` | Update student status |
| GET | `/api/admin/drives` | List placement drives |
| PUT | `/api/admin/drives/<drive_id>/status` | Update placement drive status |
| GET | `/api/admin/applications` | List applications |

The `<drive_id>`, `<user_id>`, and `<app_id>` values are resource identifiers that must be replaced with actual IDs.

### Example API Request

Use the following command to test student registration:

```bash
curl -X POST http://127.0.0.1:5000/api/register/student \
  -H "Content-Type: application/json" \
  -d '{"email":"student@example.com","password":"your-password","full_name":"Example Student"}'
```

Successful registration returns a JSON response and an HTTP success status.

Protected endpoints require an authenticated session. For command-line testing, preserve the session cookie received at login and send it with subsequent requests. The current API is not yet configured for Bearer-token authentication.

## 8. Database

The application uses SQLite with Flask-SQLAlchemy.

The configured database URI is:

```text
sqlite:///placement_portal.db
```

Database tables are initialized using `db.create_all()` when the Flask application is started directly through `app.py`.

The models represent users, student profiles, company profiles, placement drives, and applications.

For future production deployments, database migrations and a production-grade database configuration are recommended.

## 9. Background Jobs and Email

The project includes Celery, Redis, and email-related task files.

The configured Redis broker and result backend are:

```text
redis://localhost:6379/0
```

To use background tasks, start a Redis server and configure the Celery worker according to `tasks/celery_worker.py`. Configure MailHog or another supported mail server if email delivery is required.

Background jobs are an optional component of this project. Verify that the worker and individual tasks are configured correctly before relying on them.

## 10. Security Considerations

- Passwords are hashed before storage.
- Protected routes use Flask-Login.
- Role checks are implemented for student, company, and administrator operations.
- CORS is configured for specified frontend development origins.
- Secret keys and credentials should be stored outside the repository.
- Default development credentials must not be used in production.

Further work is needed to implement and verify JWT access-token authentication and configure Flask-Security if those are required by the project specification.

## 11. Future Improvements

- Implement JWT access-token authentication for API clients.
- Configure Flask-Security for the required authentication and security features.
- Add automated API and frontend tests.
- Complete and verify background email tasks.
- Add database migrations.
- Improve input validation and error handling.
- Provide API examples and screenshots for each user role.

## 12. Learning Outcomes

This project provides practical experience with:

- Full-stack web application architecture.
- Flask backend development and REST-style APIs.
- SQLAlchemy database modeling.
- Authentication and role-based authorization.
- Vue.js components and routing.
- Axios-based frontend/backend integration.
- Asynchronous processing with Celery and Redis.
- GitHub version control and project documentation.

## 13. License

Add an appropriate license before distributing this project publicly. If this is an academic project, follow the applicable course and institutional submission guidelines.
