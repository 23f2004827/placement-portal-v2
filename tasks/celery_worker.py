import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from celery import Celery
import csv
from io import StringIO
from app import create_app

flask_app = create_app()
celery_app = Celery('tasks.celery_worker', broker=flask_app.config['CELERY_BROKER_URL'])
celery_app.conf.update(flask_app.config)

@celery_app.task
def export_student_applications_csv(user_id):
    with flask_app.app_context():
        from models import User, Application
        student = User.query.get(user_id)
        if not student or student.role != 'student': return False
        
        applications = student.student_profile.applications
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Student ID', 'Company Name', 'Drive Title', 'Application Status', 'Application Date'])
        
        for app in applications:
            drive = app.drive
            writer.writerow([
                student.id,
                drive.company.company_name if drive.company else '',
                drive.job_title,
                app.status,
                app.application_date.isoformat()
            ])
        
        # Send the CSV via email to the student
        from flask_mail import Message
        
        msg = Message(
            subject="Your Placement Portal Application History (CSV Export)",
            recipients=[student.email],
            body="Hello,\n\nPlease find attached the CSV export of your application history.\n\nBest regards,\nPlacement Portal"
        )
        msg.attach(
            filename="applications.csv", 
            content_type="text/csv", 
            data=output.getvalue().encode('utf-8'),
            disposition="attachment"
        )
        
        try:
            flask_app.mail.send(msg)
            print(f"Successfully emailed CSV export to {student.email}")
        except Exception as e:
            print(f"Failed to send email to {student.email}: {e}")
            
        return True

@celery_app.task
def send_status_update_email(student_email, new_status, company_name, job_title):
    with flask_app.app_context():
        from flask_mail import Message
        msg = Message(
            subject=f"Application Update: {company_name}",
            recipients=[student_email],
            body=f"Hello,\n\nYour application status for the role of '{job_title}' at {company_name} has been updated to: {new_status}.\n\nBest regards,\nPlacement Portal"
        )
        try:
            flask_app.mail.send(msg)
            print(f"Sent status update email to {student_email}")
        except Exception as e:
            print(f"Failed to send email: {e}")
        return True