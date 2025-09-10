import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import re

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Valid values for validation
VALID_STATUSES = {'pending', 'in-progress', 'resolved'}
VALID_PRIORITIES = {'low', 'medium', 'high'}

# Initialize database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user'
    )''')
    
    # Messages table
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        predicted_priority TEXT NOT NULL,
        final_priority TEXT DEFAULT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    
    # Create default admin user if specified via environment
    admin_email = os.environ.get('ADMIN_EMAIL')
    admin_password = os.environ.get('ADMIN_PASSWORD')
    if admin_email and admin_password:
        c.execute("SELECT id FROM users WHERE email = ?", (admin_email,))
        if not c.fetchone():
            admin_hash = generate_password_hash(admin_password)
            c.execute("INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
                     (admin_email, admin_hash, 'admin'))
    
    conn.commit()
    conn.close()

# Load ML model
def load_model():
    try:
        # Try models directory first, then root directory
        try:
            return joblib.load('models/priority_model.pkl')
        except FileNotFoundError:
            return joblib.load('priority_model.pkl')
    except Exception as e:
        print(f"Warning: Could not load ML model: {e}")
        return None

# Text preprocessing
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Predict priority using ML model
def predict_priority(content):
    model_data = load_model()
    if not model_data:
        return 'medium'  # Default priority
    
    model = model_data['model']
    vectorizer = model_data['vectorizer']
    
    processed_text = preprocess_text(content)
    text_vector = vectorizer.transform([processed_text])
    priority = model.predict(text_vector)[0]
    return priority

# Database helper functions
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_user_by_email(email):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return user

# Authentication decorator
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = get_user_by_id(session['user_id'])
        if not user or user['role'] != 'admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if get_user_by_email(email):
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        password_hash = generate_password_hash(password)
        conn = get_db_connection()
        conn.execute("INSERT INTO users (email, password_hash) VALUES (?, ?)",
                    (email, password_hash))
        conn.commit()
        conn.close()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = get_user_by_email(email)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_role'] = user['role']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if session.get('user_role') == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('user_dashboard'))

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    conn = get_db_connection()
    messages = conn.execute('''
        SELECT * FROM messages 
        WHERE user_id = ? 
        ORDER BY timestamp DESC
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('user_dashboard.html', messages=messages)

@app.route('/user/submit', methods=['GET', 'POST'])
@login_required
def submit_message():
    if request.method == 'POST':
        content = request.form['content']
        predicted_priority = predict_priority(content)
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO messages (user_id, content, predicted_priority)
            VALUES (?, ?, ?)
        ''', (session['user_id'], content, predicted_priority))
        conn.commit()
        conn.close()
        
        flash('Message submitted successfully!', 'success')
        return redirect(url_for('user_dashboard'))
    
    return render_template('submit_message.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    conn = get_db_connection()
    
    # Priority order for sorting
    priority_order = {'high': 3, 'medium': 2, 'low': 1}
    
    messages = conn.execute('''
        SELECT m.*, u.email as user_email 
        FROM messages m
        JOIN users u ON m.user_id = u.id
        ORDER BY m.status ASC, m.timestamp DESC
    ''').fetchall()
    
    # Sort by priority (use final_priority if set, otherwise predicted_priority)
    def get_priority_value(msg):
        priority = msg['final_priority'] or msg['predicted_priority']
        return priority_order.get(priority, 2)
    
    messages = sorted(messages, key=get_priority_value, reverse=True)
    conn.close()
    
    return render_template('admin_dashboard.html', messages=messages)

@app.route('/admin/update_message/<int:message_id>', methods=['POST'])
@admin_required
def update_message(message_id):
    status = request.form.get('status')
    priority = request.form.get('priority')
    
    # Validate inputs
    if status and status not in VALID_STATUSES:
        flash('Invalid status value', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if priority and priority not in VALID_PRIORITIES:
        flash('Invalid priority value', 'error')
        return redirect(url_for('admin_dashboard'))
    
    conn = get_db_connection()
    
    updates = []
    params = []
    
    if status:
        updates.append("status = ?")
        params.append(status)
    
    if priority:
        updates.append("final_priority = ?")
        params.append(priority)
    
    if updates:
        params.append(message_id)
        query = f"UPDATE messages SET {', '.join(updates)} WHERE id = ?"
        conn.execute(query, params)
        conn.commit()
    
    conn.close()
    
    flash('Message updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    init_db()
    # Use debug=False for production safety
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)