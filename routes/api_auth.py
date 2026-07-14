from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, current_user, login_required
from models import db, User, StudentProfile, CompanyProfile
from werkzeug.security import generate_password_hash, check_password_hash

api_auth_bp = Blueprint('api_auth', __name__, url_prefix='/api')

@api_auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        if not user.is_active:
            return jsonify({"message": "Your account has been blacklisted or deactivated."}), 403
        
        login_user(user)
        return jsonify({
            "message": "Logged in successfully",
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
                "is_approved": user.is_approved
            }
        }), 200
        
    return jsonify({"message": "Invalid email or password"}), 401


@api_auth_bp.route('/register/student', methods=['POST'])
def register_student():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    
    new_user = User(
        email=email,
        password=hashed_password,
        full_name=full_name,
        role='student',
        is_active=True,
        is_approved=True # Students don't need admin approval to login
    )
    db.session.add(new_user)
    db.session.commit()

    student_profile = StudentProfile(user_id=new_user.id)
    db.session.add(student_profile)
    db.session.commit()

    return jsonify({"message": "Student registered successfully!"}), 201


@api_auth_bp.route('/register/company', methods=['POST'])
def register_company():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name') # HR Representative name
    company_name = data.get('company_name')
    hr_contact = data.get('hr_contact')
    website = data.get('website')

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    
    new_user = User(
        email=email,
        password=hashed_password,
        full_name=full_name,
        role='company',
        is_active=True,
        is_approved=False # Admin must approve companies
    )
    db.session.add(new_user)
    db.session.commit()

    company_profile = CompanyProfile(
        user_id=new_user.id,
        company_name=company_name,
        hr_contact=hr_contact,
        website=website
    )
    db.session.add(company_profile)
    db.session.commit()

    return jsonify({"message": "Company registered successfully! Awaiting admin approval."}), 201


@api_auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

@api_auth_bp.route('/me', methods=['GET'])
@login_required
def me():
    return jsonify({
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "role": current_user.role,
            "is_approved": current_user.is_approved
        }
    }), 200