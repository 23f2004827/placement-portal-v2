from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import db, CompanyProfile, PlacementDrive, Application
from datetime import datetime

company_api_bp = Blueprint('company_api', __name__, url_prefix='/api/company')

def is_company():
    return current_user.is_authenticated and current_user.role == 'company'

@company_api_bp.route('/profile', methods=['GET', 'PUT'])
@login_required
def profile():
    if not is_company(): return jsonify({"message": "Unauthorized"}), 403
    
    profile = current_user.company_profile
    if request.method == 'GET':
        return jsonify({
            "company_name": profile.company_name,
            "hr_contact": profile.hr_contact,
            "website": profile.website,
            "is_approved": current_user.is_approved
        }), 200

    if request.method == 'PUT':
        data = request.get_json()
        profile.company_name = data.get('company_name', profile.company_name)
        profile.hr_contact = data.get('hr_contact', profile.hr_contact)
        profile.website = data.get('website', profile.website)
        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 200


@company_api_bp.route('/drives', methods=['GET', 'POST'])
@login_required
def manage_drives():
    if not is_company(): return jsonify({"message": "Unauthorized"}), 403
    
    # Check if company is approved
    if not current_user.is_approved:
        return jsonify({"message": "Your company profile must be approved by the admin before creating placement drives."}), 403

    if request.method == 'GET':
        drives = current_user.company_profile.drives
        result = []
        for drive in drives:
            result.append({
                "id": drive.id,
                "job_title": drive.job_title,
                "job_description": drive.job_description,
                "deadline": drive.application_deadline.isoformat(),
                "status": drive.status,
                "applicant_count": len(drive.applications)
            })
        return jsonify(result), 200

    if request.method == 'POST':
        data = request.get_json()
        deadline_str = data.get('application_deadline')
        deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00')) if deadline_str else None

        new_drive = PlacementDrive(
            company_profile_id=current_user.company_profile.id,
            job_title=data.get('job_title'),
            job_description=data.get('job_description'),
            eligible_branches=data.get('eligible_branches', ''),
            min_cgpa=data.get('min_cgpa', 0.0),
            eligible_years=data.get('eligible_years', ''),
            application_deadline=deadline,
            status='Pending' # Needs admin approval
        )
        db.session.add(new_drive)
        db.session.commit()
        return jsonify({"message": "Placement drive created successfully. Awaiting admin approval."}), 201


@company_api_bp.route('/drives/<int:drive_id>/applications', methods=['GET'])
@login_required
def get_drive_applications(drive_id):
    if not is_company(): return jsonify({"message": "Unauthorized"}), 403
    
    drive = PlacementDrive.query.filter_by(id=drive_id, company_profile_id=current_user.company_profile.id).first()
    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    applications = drive.applications
    result = []
    for app in applications:
        student = app.student.user
        student_prof = app.student
        result.append({
            "application_id": app.id,
            "student_name": student.full_name,
            "student_email": student.email,
            "branch": student_prof.branch,
            "cgpa": student_prof.cgpa,
            "resume_path": student_prof.resume_path,
            "status": app.status,
            "application_date": app.application_date.isoformat()
        })
    return jsonify(result), 200

@company_api_bp.route('/applications/<int:app_id>/status', methods=['PUT'])
@login_required
def update_application_status(app_id):
    if not is_company(): return jsonify({"message": "Unauthorized"}), 403
    
    data = request.get_json()
    status = data.get('status') # 'Shortlisted', 'Selected', 'Rejected'

    application = Application.query.get(app_id)
    if not application or application.drive.company_profile_id != current_user.company_profile.id:
        return jsonify({"message": "Application not found"}), 404

    application.status = status
    db.session.commit()
    
    # Trigger background email task
    from tasks.celery_worker import send_status_update_email
    student_email = application.student.user.email
    company_name = application.drive.company.company_name
    job_title = application.drive.job_title
    
    send_status_update_email.delay(student_email, status, company_name, job_title)
    
    return jsonify({"message": f"Application status updated to {status} and notification sent"}), 200
