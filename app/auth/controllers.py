from flask import Blueprint, request, render_template, url_for, flash, session, redirect
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from app import login_manager
from app.auth.models import User

mod_auth = Blueprint('auth', __name__, url_prefix='/admin', template_folder='templates')

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

@mod_auth.route('/')
@mod_auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email     = request.form['email']
        password  = request.form['password']
        if email == "" and password == "":
            flash('Email and password should be mandatory', category="danger")
        else:
            user = User.query.filter_by(email=email).first()
            if user is not None and check_password_hash(user.password, password):
                login_user(user)
                session['logged_in'] = True
                session['uid'] = user.iduser
                return redirect(url_for('dashboard.admin_dashboard'))
            else:
                flash('Please check your login details and try again.', category="danger")
                return redirect(url_for('auth.login'))

    return render_template('login.html')

@mod_auth.route('/logout/', methods=['GET'])
@login_required
def logout():
    logout_user()
    session['logged_in'] = None
    session['uid'] = None
    flash('You have successfully been logged out.', category='success')
    return redirect(url_for('auth.login'))