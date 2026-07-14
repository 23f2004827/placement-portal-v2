from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import db, StudentProfile, PlacementDrive, Application
from datetime import datetime

student_api_bp = Blueprint('student_api', __name__, url_prefix='/api/student')

def is_student():
    return current_user.is_authenticated and current_user.role == 'student'

@student_api_bp.route('/profile', methods=['GET', 'PUT'])
@login_required
def profile():
    if not is_student(): return jsonify({"message": "Unauthorized"}), 403
    
    profile = current_user.student_profile
    if request.method == 'GET':
        return jsonify({
            "full_name": current_user.full_name,
            "branch": profile.branch,
            "cgpa": profile.cgpa,
            "graduation_year": profile.graduation_year,
            "resume_path": profile.resume_path
        }), 200

    if request.method == 'PUT':
        data = request.get_json()
        current_user.full_name = data.get('full_name', current_user.full_name)
        profile.branch = data.get('branch', profile.branch)
        profile.cgpa = data.get('cgpa', profile.cgpa)
        profile.graduation_year = data.get('graduation_year', profile.graduation_year)
        profile.resume_path = data.get('resume_path', profile.resume_path)
        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 200


@student_api_bp.route('/drives', methods=['GET'])
@login_required
def get_drives():
    if not is_student(): return jsonify({"message": "Unauthorized"}), 403
    
    # Only show approved drives where deadline has not passed
    drives = PlacementDrive.query.filter_by(status='Approved').all()
    result = []
    for drive in drives:
        result.append({
            "id": drive.id,
            "company_name": drive.company.company_name,
            "job_title": drive.job_title,
            "job_description": drive.job_description,
            "eligible_branches": drive.eligible_branches,
            "min_cgpa": drive.min_cgpa,
            "eligible_years": drive.eligible_years,
            "deadline": drive.application_deadline.isoformat() if drive.application_deadline else None
        })
    return jsonify(result), 200

@student_api_bp.route('/drives/<int:drive_id>/apply', methods=['POST'])
@login_required
def apply_to_drive(drive_id):
    if not is_student(): return jsonify({"message": "Unauthorized"}), 403
    
    drive = PlacementDrive.query.filter_by(id=drive_id, status='Approved').first()
    if not drive:
        return jsonify({"message": "Drive not found or not open"}), 404

    # Check if already applied
    existing_app = Application.query.filter_by(student_profile_id=current_user.student_profile.id, drive_id=drive_id).first()
    if existing_app:
        return jsonify({"message": "Already applied to this drive"}), 400

    # Eligibility check logic can be added here
    # For now, just apply directly
    application = Application(
        student_profile_id=current_user.student_profile.id,
        drive_id=drive_id,
        status='Applied'
    )
    db.session.add(application)
    db.session.commit()
    return jsonify({"message": "Successfully applied to the placement drive"}), 201


@student_api_bp.route('/applications', methods=['GET'])
@login_required
def get_applications():
    if not is_student(): return jsonify({"message": "Unauthorized"}), 403
    
    applications = current_user.student_profile.applications
    result = []
    for app in applications:
        drive = app.drive
        result.append({
            "application_id": app.id,
            "company_name": drive.company.company_name,
            "job_title": drive.job_title,
            "status": app.status,
            "application_date": app.application_date.isoformat()
        })
    return jsonify(result), 200

@student_api_bp.route('/export', methods=['POST'])
@login_required
def export_applications():
    if not is_student(): return jsonify({"message": "Unauthorized"}), 403
    
    # Trigger Celery task
    try:
        from tasks.celery_worker import export_student_applications_csv
        task = export_student_applications_csv.delay(current_user.id)
        return jsonify({"message": "Export job triggered.", "task_id": task.id}), 202
    except Exception as e:
        return jsonify({"message": "Failed to trigger export task", "error": str(e)}), 500
