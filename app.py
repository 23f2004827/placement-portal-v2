from flask import Flask
from config import Config
from models import db
from flask_login import LoginManager
from flask_cors import CORS
from flask_mail import Mail

# Blueprints
from routes.api_auth import api_auth_bp
from routes.admin import admin_api_bp
from routes.company import company_api_bp
from routes.student import student_api_bp

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins=["http://localhost:8080", "http://127.0.0.1:8080", "http://192.168.1.6:8080"], allow_headers=["Authorization", "Content-Type"])
    app.config.from_object(Config)

    db.init_app(app)
    
    # Initialize Flask-Mail
    mail = Mail(app)
    app.mail = mail

    login_manager = LoginManager()
    login_manager.init_app(app)

    from models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(api_auth_bp)
    app.register_blueprint(admin_api_bp)
    app.register_blueprint(company_api_bp)
    app.register_blueprint(student_api_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
        
        # Create a predefined admin user if it doesn't exist
        from models import User
        from werkzeug.security import generate_password_hash
        
        admin_email = "admin@example.com"
        existing_admin = User.query.filter_by(email=admin_email).first()

        if not existing_admin:
            admin_plaintext_password = "admin123"
            hashed_admin_password = generate_password_hash(admin_plaintext_password, method='pbkdf2:sha256')
            admin = User(
                email=admin_email,
                password=hashed_admin_password,
                full_name="Admin",
                role="admin",
                is_active=True,
                is_approved=True # Admin is always approved
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created successfully with hashed password!")
            
    app.run(debug=True)
