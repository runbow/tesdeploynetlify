from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
import pandas as pd
import sqlite3
import os


# We use a Blueprint to connect this to app.py later
dashboard_bp = Blueprint('dashboard', __name__)

# --- 1. THE PROCESSOR FUNCTIONS (Logic) ---

def process_hourly_sum(start_date, end_date):
    # Your real Pandas logic will go here
    return f"Processed data {start_date} to {end_date}: Total Hourly Sum calculated."

def process_daily_avg(start_date, end_date):
    return f"Processed data {start_date} to {end_date}: Daily Averages generated."

# --- 2. THE TASK HANDLER (The Route) ---

@dashboard_bp.route('/dashboard')
@login_required
def show_dashboard():
    # Fetch paths from DB for the current user
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    rows = conn.execute('SELECT base_path, allowed_start_date, allowed_end_date FROM allowed_data WHERE user_id = ?', 
                        (current_user.id,)).fetchall()
    conn.close()
    
    scopes = [{'start_date': r['allowed_start_date'], 'end_date': r['allowed_end_date']} for r in rows]
    return render_template('dashboard.html', scopes=scopes)

@dashboard_bp.route('/run-task', methods=['POST'])
@login_required
def task_handler():
    data = request.json
    start_date = data.get('start_date', [])
    end_date = data.get('end_date', [])
    method = data.get('method', '')

    if not start_date or not end_date:
        return jsonify({'success': False, 'error': 'No data has been assigned!'})

    # Direct "Throw" to the processor functions in the same file
    if method == 'hourly':
        result_message = process_hourly_sum(start_date, end_date)
    elif method == 'daily':
        result_message = process_daily_avg(start_date, end_date)
    else:
        result_message = "Unknown method selected."

    return jsonify({
        'success': True,
        'method_executed': method,
        'result': result_message
    })