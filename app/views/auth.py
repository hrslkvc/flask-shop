import sqlalchemy.exc
from flask import Blueprint, request, jsonify
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db
from flask_jwt_extended import create_access_token

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/register', methods=('POST',))
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({'error': 'username and password are required'}), 400

    try:
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict())

    except sqlalchemy.exc.IntegrityError:
        return jsonify({'error': 'User with the provided username already exists'}), 400


@auth.route('/login', methods=('POST',))
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({'error': 'username and password are required'}), 400

    user = User.query.filter_by(username=username).first()

    if check_password_hash(user.password, password):
        token = create_access_token(identity=username)
        return jsonify({'access_token': token})

    return jsonify({'error': 'Invalid credentials'})
