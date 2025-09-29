from flask import Blueprint, render_template, request, jsonify
from . import db
from .models import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main.route('/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'email' not in data:
            return jsonify({'error': 'Username and email are required'}), 400
            
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully', 'user': {'id': new_user.id, 'username': new_user.username, 'email': new_user.email}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@main.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Flask app is running!'})
