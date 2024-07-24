from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean
from flask_cors import CORS
from functools import wraps
import pytz
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todos los orígenes por defecto
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SECRET_KEY'] = 'supersecretkey'
db = SQLAlchemy(app)

# Definimos la zona horaria de la Ciudad de México
cdmx_tz = pytz.timezone('America/Mexico_City')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    message = db.Column(db.Text, nullable=True)
    read = db.Column(Boolean, default=False)
    received_at = db.Column(db.DateTime, default=lambda: datetime.now(cdmx_tz))
    opened_at = db.Column(db.DateTime, nullable=True)

    __table_args__ = (db.UniqueConstraint('name', 'email', 'phone', 'message', name='unique_message_constraint'),)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/add_message', methods=['POST'])
def add_message():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message')

    if not name or not email:
        return jsonify({'error': 'Name and Email are required'}), 400

    existing_message = Message.query.filter_by(name=name, email=email, phone=phone, message=message).first()
    if existing_message:
        return jsonify({'error': 'Duplicate message'}), 400

    new_message = Message(name=name, email=email, phone=phone, message=message)
    db.session.add(new_message)
    db.session.commit()

    return jsonify({'message': 'Message added successfully'}), 201

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'secreto':
            session['logged_in'] = True
            return redirect(url_for('view_messages'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/messages')
@login_required
def view_messages():
    messages = Message.query.all()
    return render_template('messages.html', messages=messages)

@app.route('/message/<int:message_id>')
@login_required
def view_message(message_id):
    message = Message.query.get_or_404(message_id)
    if not message.read:
        message.read = True
        message.opened_at = datetime.now(cdmx_tz)
        db.session.commit()
    return render_template('message.html', message=message)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
