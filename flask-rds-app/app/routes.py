from flask import Blueprint, request, jsonify, abort
from .models import db, User

# Create a Blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or not data.get('name'):
        abort(400, description="Name is required.") # Use description for better error messages

    name = data.get('name')
    if User.query.filter_by(name=name).first():
         abort(409, description=f"User with name '{name}' already exists.") # Conflict

    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": f"User {name} added!", "user": user.to_dict()}), 201 # Return created user and 201 status

@api_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@api_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(User, id) # Use db.session.get for primary key lookup
    if not user:
        abort(404, description="User not found.")
    return jsonify(user.to_dict())

@api_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.session.get(User, id)
    if not user:
        abort(404, description="User not found.")

    data = request.get_json()
    if not data or not data.get('name'):
        abort(400, description="Name is required.")

    new_name = data.get('name')
    # Optional: Check if the new name conflicts with another user
    existing_user = User.query.filter(User.name == new_name, User.id != id).first()
    if existing_user:
        abort(409, description=f"Another user with name '{new_name}' already exists.")

    user.name = new_name
    db.session.commit()
    return jsonify({"message": f"User {id} updated!", "user": user.to_dict()})

@api_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)
    if not user:
        abort(404, description="User not found.")

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {id} deleted!"})

# Optional: Add a simple health check endpoint
@api_bp.route('/health', methods=['GET'])
def health_check():
    # Can add a db ping here later if needed
    return jsonify({"status": "ok"})
