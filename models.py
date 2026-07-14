from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

# Initialize database
db = SQLAlchemy()

# Unified User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    
    # Roles: 'admin', 'company', 'student'
    role = db.Column(db.String(20), nullable=False)
    
    # Status flags
    is_active = db.Column(db.Boolean, default=True) # Used for blacklisting
    is_approved = db.Column(db.Boolean, default=False) # For companies, admin must approve

    # Relationships
    company_profile = db.relationship('CompanyProfile', backref='user', uselist=False, cascade="all, delete-orphan")
    student_profile = db.relationship('StudentProfile', backref='user', uselist=False, cascade="all, delete-orphan")


# Company Profile
class CompanyProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(150), nullable=False)
    hr_contact = db.Column(db.String(150))
    website = db.Column(db.String(255))
    
    # Relationships
    drives = db.relationship('PlacementDrive', backref='company', cascade="all, delete-orphan", lazy=True)


# Student Profile
class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    branch = db.Column(db.String(100))
    cgpa = db.Column(db.Float)
    graduation_year = db.Column(db.Integer)
    resume_path = db.Column(db.String(255))
    
    # Relationships
    applications = db.relationship('Application', backref='student', cascade="all, delete-orphan", lazy=True)


# Placement Drive
class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_profile_id = db.Column(db.Integer, db.ForeignKey('company_profile.id'), nullable=False)
    job_title = db.Column(db.String(150), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    
    # Eligibility
    eligible_branches = db.Column(db.String(255)) # Comma separated
    min_cgpa = db.Column(db.Float)
    eligible_years = db.Column(db.String(255)) # Comma separated

    application_deadline = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Status: 'Pending', 'Approved', 'Closed'
    status = db.Column(db.String(20), default='Pending')

    # Relationships
    applications = db.relationship('Application', backref='drive', cascade="all, delete-orphan", lazy=True)


# Application
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_profile_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'), nullable=False)
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Status: 'Applied', 'Shortlisted', 'Selected', 'Rejected'
    status = db.Column(db.String(20), default='Applied')
