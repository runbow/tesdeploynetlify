from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
import sqlite3
from auth_utils import admin_required # Import your gatekeeper

app = Flask(__name__)
app.secret_key = 'dev_key_123' 

# Register the blueprint
from main_dashboard import dashboard_bp
app.register_blueprint(dashboard_bp)

from admin import admin_bp
app.register_blueprint(admin_bp)

# --- Flask-Login Setup ---
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role # Store the role name

    def is_admin(self):
        return self.role == 'admin'

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    # Join users and roles to load the role name directly
    user = conn.execute('''
        SELECT u.id, u.username, r.role_name 
        FROM users u 
        JOIN roles r ON u.role_id = r.id 
        WHERE u.id = ?''', (user_id,)).fetchone()
    conn.close()
    
    if user:
        return User(user['id'], user['username'], user['role_name'])
    return None

# --- Routes ---

@app.route('/')
def home():
    #return redirect(url_for('login'))
    return "Ok bisa jalan"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        conn.row_factory = sqlite3.Row
        # Get user along with their role_id
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if user and check_password_hash(user['password'], password):
            # Fetch role name
            role = conn.execute('SELECT role_name FROM roles WHERE id = ?', (user['role_id'],)).fetchone()
            conn.close()
            
            user_obj = User(user['id'], user['username'], role['role_name'])
            login_user(user_obj)
            
            # Redirect admins to admin dashboard, others to main
            if user_obj.is_admin():
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('dashboard.show_dashboard'))
        
        conn.close()
        return "Login Failed: Wrong username or password"
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

#if __name__ == '__main__':
    #app.run(debug=True)
