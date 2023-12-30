from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, redirect, flash, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from werkzeug.security import check_password_hash
import mysql.connector
# from . import app, db
import os

# Initialize Flask app
app = Flask(__name__)

# Configure app
app.config['SECRET_KEY'] = '38904621054367'
DATABASE_URL="mysql+mysqlconnector://Olive357:Olive0880@Olive357.mysql.pythonanywhere-services.com/Olive357?host=%"
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'odomenget@gmail.com'
app.config['MAIL_PASSWORD'] = 'qdhj sguf dkec lxfa'
app.config['DEBUG'] = True

# Initialize SQLAlchemy, LoginManager, and Mail
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
mail = Mail(app)

# Define User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(255), nullable=False)
    registration_date = db.Column(db.Date, nullable=False)
    token = db.Column(db.String(255), nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    validation_date = db.Column(db.DateTime)

    def is_validated(self):
        return self.validation_date is not None

#    __tablename__ = 'users'  # Add this line

# Define User schema for serialization
class UserSchema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255))
    role = db.Column(db.String(255))
    registration_date = db.Column(db.Date)
    validation_date = db.Column(db.DateTime)

# Initialize User schema
user_schema = UserSchema()
users_schema = UserSchema()

# Define login manager loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
'''
@login_manager.loader
def load_user(user_id):
    return User.query.get(int(user_id))
'''
# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/code')
def code():
    return render_template('code.txt')

@app.route('/contact', methods=['POST'])
def process_contact_form():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    send_email('Nouveau message de contact', 'domenget@gmail.com', ['odomenget@gmail.com'], f'Nom: {name}\nAdresse e-mail: {email}\nMessage: {message}', f'<p><strong>Nom:</strong> {name}</p><p><strong>Adresse e-mail:</strong> {email}</p><p><strong>Message:</strong></p><p>{message}</p>')
    flash(('success', 'Votre message a été envoyé avec succès!'))
    return redirect(url_for('contact'))

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        role = request.form['role']

        # Check if user already exists
        user = User.query.filter_by(username=username).first()
        if user is not None:
            flash('Username already exists.')
            return redirect(url_for('register'))

        user = User.query.filter_by(table_name='users', email=email).first()
        if user is not None:
            flash('Email already exists.')
            return redirect(url_for('register'))

        # Create new user
        user = User(
            username=username,
            password=password,
            email=email,
            role= 'user',
            registration_date=datetime.utcnow(),
            token=os.urandom(24).hex(),
            expiration_date=datetime.utcnow() + timedelta(minutes=15)
        )

        # Save user to database
        db.session.add(user)
        db.session.commit()

        # Send email validation link
        msg = Message('Email validation', recipients=[email])
        msg.body = f'Please click the following link to validate your email: {url_for("validate_email", token=user.token, _external=True)}'
        mail.send(msg)

        flash('Registration successful. Please check your email for validation link.')
        return redirect(url_for('index'))

    return render_template('register.html')
'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    from app.models import User

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user is None or not user.check_password(password):
            flash('Invalid email or password')
            return redirect(url_for('login'))

        if not user.is_validated():
            flash('Email not validated. Please check your email for validation link.')
            return redirect(url_for('index'))

        # Set a session cookie to keep the user logged in
        session['user_id'] = user.id

        login_user(user)

        return redirect(url_for('index'))

    return render_template('login.html')
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        email = request.form['email'].lower()
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')

@app.route('/validate_email/<token>')
def validate_email(token):
    user = User.query.filter_by(token=token).first()

    if user is None or user.expiration_date < datetime.utcnow():
        abort(404)

    user.expiration_date = None
    user.validation_date = datetime.utcnow()
    db.session.commit()

    flash('Email validated successfully.')
    return redirect(url_for('index'))

@app.route('/personal_space')
@login_required
def personal_space():
    user = User.query.filter_by(id=current_user.id).first()
    if not user.is_validated():
        flash('Email not validated. Please check your email for validation link.')
        return redirect(url_for('index'))

    if user:
        # Set a session cookie to keep the user logged in
        session['user_id'] = user.id

        login_user(user)
        return redirect(url_for('personal_space'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
