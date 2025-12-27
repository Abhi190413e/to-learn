from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from first.chatbot import Chatbot
from first.models import db, User, LoginLog, Course, Video, Meeting
import os
from datetime import datetime

app = Flask(__name__)
# Use environment variables for sensitive info, with fallbacks for local dev
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key_change_in_prod')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///academy.db')
# Fix for Render/Heroku postgres URLs starting with postgres://
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

bot = Chatbot("myfrnd")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_user():
    return dict(user=current_user)

def create_tables():
    db.create_all()
    # Create admin user if not exists
    if not User.query.filter_by(username='admin').first():
        hashed_pw = generate_password_hash('admin123', method='pbkdf2:sha256')
        admin = User(username='admin', password_hash=hashed_pw, is_admin=True)
        db.session.add(admin)
        db.session.commit()

with app.app_context():
    create_tables()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            # Log the login
            new_log = LoginLog(user_id=user.id, ip_address=request.remote_addr)
            db.session.add(new_log)
            db.session.commit()
            
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    logs = LoginLog.query.order_by(LoginLog.timestamp.desc()).limit(50).all()
    return render_template('dashboard.html', logs=logs)

@app.route('/admin/add-course', methods=['GET', 'POST'])
@login_required
def add_course():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        image_url = request.form.get('image_url')
        new_course = Course(title=title, description=description, image_url=image_url)
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for('courses'))
    return render_template('add_course.html')

@app.route('/admin/add-video', methods=['GET', 'POST'])
@login_required
def add_video():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    courses = Course.query.all()
    if request.method == 'POST':
        course_id = request.form.get('course_id')
        title = request.form.get('title')
        url = request.form.get('url')
        new_video = Video(course_id=course_id, title=title, url=url)
        db.session.add(new_video)
        db.session.commit()
        return redirect(url_for('courses'))
    return render_template('add_video.html', courses=courses)

@app.route('/admin/add-meeting', methods=['GET', 'POST'])
@login_required
def add_meeting():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    if request.method == 'POST':
        title = request.form.get('title')
        date = request.form.get('date')
        time = request.form.get('time')
        link = request.form.get('link')
        new_meeting = Meeting(title=title, date=date, time=time, link=link)
        db.session.add(new_meeting)
        db.session.commit()
        return redirect(url_for('live_meets'))
    return render_template('add_meeting.html')

@app.route('/courses')
def courses():
    all_courses = Course.query.all()
    return render_template('courses.html', courses=all_courses)

@app.route('/live-meets')
def live_meets():
    meetings = Meeting.query.all()
    return render_template('live_meets.html', meetings=meetings)

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"response": "Please say something!"})
    
    response = bot.get_response(user_input)
    return jsonify({"response": response})

@app.route('/sw.js')
def service_worker():
    return send_from_directory('static', 'sw.js')

@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('assets', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
