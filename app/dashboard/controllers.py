from flask import Blueprint, request, render_template, url_for, redirect, flash
from flask_login import login_required

mod_dashboard = Blueprint('dashboard', __name__, url_prefix='/admin', template_folder='templates')

@mod_dashboard.route('/dashboard/')
@login_required
def admin_dashboard():
    return render_template('dashboard.html')