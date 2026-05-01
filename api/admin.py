from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from auth_utils import admin_required
from werkzeug.security import generate_password_hash
import sqlite3

# Create the blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Renders the main Admin Shell"""
    return render_template('admin_dashboard.html')

@admin_bp.route('/view/<view_name>')
@login_required
@admin_required
def get_admin_view(view_name):
    """
    Handles dynamic loading of forms into the main-content div.
    Called by JavaScript fetch() in admin_dashboard.html
    """
    if view_name == 'create-user':
        return render_template('forms/create_user.html')
    
    return "View not found", 404

@admin_bp.route('/create-user', methods=['POST'])
@login_required
@admin_required
def process_create_user():
    """Handles the actual form submission from the 'Create User' form"""
    username = request.form.get('username')
    password = request.form.get('password')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    role_id = request.form.get('role_id')
    
    # Hash the password for security!
    hashed_pw = generate_password_hash(password)

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, password, role_id) 
            VALUES (?, ?, ?)
        ''', (username, hashed_pw, role_id))
        
        cursor.execute('''
            INSERT INTO allowed_data (user_id, base_path, allowed_start_date, allowed_end_date) 
            VALUES (?, ?, ?, ?)
        ''', (cursor.lastrowid, '/home/data/station_01/', start_date, end_date))
        conn.commit()
        conn.close()
        return "Success: User created!"
    except sqlite3.IntegrityError:
        return "Error: Username already exists.", 400