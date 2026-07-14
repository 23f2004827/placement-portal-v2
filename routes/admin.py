from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import db, User, CompanyProfile, PlacementDrive, Application, StudentProfile

admin_api_bp = Blueprint('admin_api', __name__, url_prefix='/api/admin')

def is_admin():
    return current_user.is_authenticated and current_user.role == 'admin'

@admin_api_bp.route('/stats', methods=['GET'])
@login_required
def get_stats():
    if not is_admin(): return jsonify({"message": "Unauthorized"}), 403
    
    total_students = User.query.filter_by(role='student').count()
    total_companies = User.query.filter_by(role='company').count()
    total_drives = PlacementDrive.query.count()

    return jsonify({
        "total_students": total_students,
        "total_companies": total_companies,
        "total_drives": total_drives
    }), 200

# --- Company Management ---
@admin_api_bp.route('/companies', methods=['GET'])
@login_required
def get_companies():
    if not is_admin(): return jsonify({"message": "Unauthorized"}), 403
    
    companies = User.query.filter_by(role='company').all()
    result = []
    for comp in companies:
        profile = comp.company_profile
        result.append({
            "id": comp.id,
            "email": comp.email,
            "company_name": profile.company_name if profile else "",
            "hr_contact": profile.hr_contact if profile else "",
            "website": profile.website if profile else "",
            "is_approved": comp.is_approved,
            "is_active": comp.is_active
        })
    return jsonify(result), 200

@admin_api_bp.route('/companies/<int:user_id>/status', methods=['PUT'])
@login_required
def update_company_status(user_id):
    if not is_admin(): return jsonify({"message": "Unauthorized"}), 403
    
    data = request.get_json()
    action = data.get('action') # 'approve', 'reject', 'blacklist', 'activate'

    company = User.query.filter_by(id=user_id, role='company').first()
    if not company:
        return jsonify({"message": "Company not found"}), 404

    if action == 'approve':
        company.is_approved = True
    elif action == 'reject':
        company.is_approved = False
    elif action == 'blacklist':
        company.is_active = False
    elif action == 'activate':
        company.is_active = True
    else:
        return jsonify({"message": "Invalid action"}), 400

    db.session.commit()
    return jsonify({"message": f"Company status updated to {action}"}), 200


# --- Student Management ---
@admin_api_bp.route('/students', methods=['GET'])
@login_required
def get_students():
    if not is_admin(): return jsonify({"message": "Unauthorized"}), 403
    
    students = User.query.filter_by(role='student').all()
    result = []
    for student in students:
        profile = student.student_profile
        result.append({
            "id": student.id,
            "email": student.email,
            "full_name": student.full_name,
            "branch": profile.branch if profile else "",
            "cgpa": profile.cgpa if profile else None,
            "graduation_year": profile.graduation_year if profile else None,
            "is_active": student.is_active
        })
    return jsonify(result), 200

@admin_api_bp.route('/students/<int:user_id>/status', methods=['PUT'])
@login_required
def update_student_status(user_id):
    if not is_admin(): return jsonify({"message": "Unauthorized"}), 403
    
    data = request.get_json()
    action = data.get('action') # 'blacklist', 'activate'

    student = User.query.filter_by(id=user_id, role='student').first()
    if not student:
        return jsonify({"message": "Student not found"}), 404

    if action == 'blacklist':
        student.is_active = False
    elif action == 'activate':
        student.is_active = True
    else:
        return jsonify({"message": "Invalid action"}), 400

    db.session.commit()
    return jsonify({"message": f"Student status updated to {action}"}), 200


# --- Placement Drive Management ---
@admin_api_bp.route('/drives', methods=['GET'])
@login_required
def get_drives():
    if not is_admin(): return jsonify({"message": "Unauthorized"}), 403
    
    drives = PlacementDrive.query.all()
    result = []
    for drive in drives:
        result.append({
            "id": drive.id,
            "company_name": drive.company.company_name if drive.company else "",
            "job_title": drive.job_title,
            "status": drive.status,
            "deadline": drive.application_deadline.isoformat() if drive.application_deadline else None
        })
    return jsonify(result), 200

@admin_api_bp.route('/drives/<int:drive_id>/status', methods=['PUT'])
@login_required
def update_drive_status(drive_id):
    if not is_admin(): return jsonify({"message": "Unauthorized"}), 403
    
    data = request.get_json()
    status = data.get('status') # 'Pending', 'Approved', 'Closed'

    if status not in ['Pending', 'Approved', 'Closed']:
        return jsonify({"message": "Invalid status"}), 400

    drive = PlacementDrive.query.get(drive_id)
    if not drive:
        return jsonify({"message": "Drive not found"}), 404

    drive.status = status
    db.session.commit()
    
    return jsonify({"message": f"Drive status updated to {status}"}), 200

# --- Applications Management ---
@admin_api_bp.route('/applications', methods=['GET'])
@login_required
def get_all_applications():
    if not is_admin(): return jsonify({"message": "Unauthorized"}), 403
    
    applications = Application.query.all()
    result = []
    for app in applications:
        student = app.student.user
        drive = app.drive
        result.append({
            "id": app.id,
            "student_name": student.full_name,
            "company_name": drive.company.company_name if drive.company else "",
            "job_title": drive.job_title,
            "status": app.status,
            "application_date": app.application_date.isoformat()
        })
    return jsonify(result), 200
