from flask import Blueprint, render_template, request, redirect, url_for, g, session
from app.models import Admin, db

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
            return redirect(url_for('dashboard'))
        else:
            error_message = "Invalid username or password"
            return render_template('index.html', error_message=error_message)
    
    return render_template('index.html')



