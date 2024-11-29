from flask import Blueprint, render_template, request, redirect, url_for, g, session,flash,jsonify
from app.models import Admin
from app.extentions import db


bp = Blueprint('login', __name__, url_prefix='/')

######### Login Page ##################

@bp.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.admin = None
    else:
        g.admin = Admin.query.get(user_id)  # Assuming session stores user_id


@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session['user_id'] = admin.admin_id  # Store the admin ID in the session
            return redirect(url_for('dashboard.dashboard'))
        else:
            error_message = "Invalid username or password"
            return render_template('index.html', error_message=error_message)
    
    return render_template('index.html')


@bp.route('/add_admin', methods=['POST'])
def add_admin():
    name = request.form.get('name')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    # Validate input
    if not name or not email or not username or not password:
        return jsonify(success=False, message="All fields are required.")

    # Check if the username or email already exists
    if Admin.query.filter_by(username=username).first():
        return jsonify(success=False, message="Username already exists.")
    if Admin.query.filter_by(email=email).first():
        return jsonify(success=False, message="Email already exists.")

    try:
        # Create new admin
        new_admin = Admin(name=name, email=email, username=username)
        new_admin.set_password(password)
        db.session.add(new_admin)
        db.session.commit()

        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, message=str(e))



@bp.route('/delete_profile', methods=['POST'])
def delete_profile():
    if g.admin is None:
        return jsonify(success=False, message="User not logged in"), 401

    try:
        # Delete the logged-in admin
        db.session.delete(g.admin)
        db.session.commit()

        # Clear the session
        session.clear()

        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, message=str(e))


@bp.route('/update_profile', methods=['POST'])
def update_profile():
    if g.admin is None:
        return jsonify(success=False, message="User not logged in"), 401

    name = request.form.get('name')
    email = request.form.get('email')
    username = request.form.get('username')

    if not name or not email or not username:
        return jsonify(success=False, message="All fields are required.")

    try:
        # Update the logged-in admin's profile
        g.admin.name = name
        g.admin.email = email
        g.admin.username = username
        db.session.commit()

        return jsonify(success=True)
    except Exception as e:
        return jsonify(success=False, message=str(e))


@bp.route('/get_profile', methods=['GET'])
def get_profile():
    if g.admin is None:
        return jsonify(success=False, message="User not logged in"), 401
    
    # Return the logged-in admin's data
    return jsonify(
        success=True,
        name=g.admin.name,
        email=g.admin.email,
        username=g.admin.username
    )
