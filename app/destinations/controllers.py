from app.trips.controllers import allowed_file
from os import abort
from flask import Blueprint, redirect, request, render_template, session, flash, url_for, escape
from flask_login import login_required
from flask_paginate import Pagination, get_page_parameter
from datetime import datetime
from config import app_config
from app.destinations.models import Destinations
from app import db
import os

mod_dest = Blueprint('destinations', __name__, url_prefix='/admin', template_folder='templates')

@mod_dest.route('/destination-list/', methods=['GET', 'POST'])
@login_required
def destination_list():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    searchdata = ""
    if request.method == 'POST' and request.form['btnsubmit'] == 'Search' and request.form['search_title'] != '':
        searchdata = request.form['search_title']
        keyword = "%{}%".format(searchdata)
        destinationObj = Destinations.query.filter(
            (Destinations.dest_title.like(keyword) | Destinations.dest_description.like(keyword))
            )
        destination_list = destinationObj.all()
        total = destinationObj.count()
    else:
        destination_list = Destinations.query.all()
        total = Destinations.query.count()
    pagination = Pagination(page=page, per_page = app_config.PER_PAGE, total=total, search=False, record_name='destinations')
    return render_template('destination-list.html', destination_list = destination_list, datetime = datetime, pagination = pagination, searchpresist=searchdata)

@mod_dest.route('/destination-add/', methods=['POST', 'GET'])
@login_required
def destination_add():
    postData = ""
    if (request.method == "POST" and request.form['btnsave'] == 'save'):
        postData = request.form
        dest_title = escape(postData['destination_title'])
        dest_description = request.form.get('destination_description')
        dest_thumb_image = request.files['destination_thumb_image']
        dest_banner_image = request.files['destination_banner_image']
        dest_highlights = request.form.get('destination_highlights')
        dest_highlight_image = request.files['destination_highlight_image']
        dest_activities = request.form.get('destination_activities')
        dest_activity_image = request.files['destination_activity_image']
        dest_location_info = escape(postData['dest_location_info'])
        dest_language_info = escape(postData['dest_language_info'])
        dest_currency_info = escape(postData['dest_currency_info'])
        dest_cuisine_info = escape(postData['dest_cuisine_info'])
        dest_airport_info = escape(postData['dest_airport_info'])
        dest_flight_duration_info = postData['dest_flight_duration_info']
        if (dest_title == ""):
            flash('Destination title should be mandatory', category="danger")
        elif (dest_description == ""):
            flash("Destination description should be mandatory", category="danger")
        elif (dest_thumb_image.filename == ""):
            flash("Destination thumb image should be mandatory", category="danger")
        elif (dest_thumb_image.filename != "" and not allowed_filename(dest_thumb_image.filename)):
            flash('Uploaded thumb image extension not allowed', category="danger")
        elif (dest_banner_image.filename == ""):
            flash("Destination banner image should be mandatory", category="danger")
        elif (dest_banner_image.filename != "" and not allowed_file(dest_banner_image.filename)):
            flash('Uploaded banner image extension not allowed', category="danger")
        elif (dest_highlights == ""):
            flash("Destination highlights should be mandatory", category="danger")
        elif (dest_highlight_image.filename == ""):
            flash("Destination should be mandatory", category='danger')
        elif (dest_highlight_image.filename != "" and not allowed_file(dest_highlight_image.filename)):
            flash('Uploaded highlight image extension not allowed', category="danger")
        elif (dest_activities == ""):
            flash("Destination activities should be mandatory", category="danger")
        elif (dest_activity_image.filename == ""):
            flash("Destination activities image should be mandatory", category="danger")
        elif (dest_activity_image.filename != "" and not allowed_file(dest_activity_image.filename)):
            flash('Uploaded acitivity image extension not allowed', category="danger")
        elif (dest_location_info == ""):
            flash("Destination location info should be mandatory", category="danger")
        elif (dest_language_info == ""):
            flash("Destination language info should be mandatory", category="danger")
        elif (dest_currency_info == ""):
            flash("Destination currency infor should be mandatory", category="danger")
        elif (dest_cuisine_info == ""):
            flash("Destination cuisine info should be mandatory", category="danger")
        elif (dest_airport_info == ""):
            flash("Destination airport infor should be mandatory", category="danger")
        elif (dest_flight_duration_info == ""):
            flash("Destination flight duration info should be mandatory", category="danger")
        else:
            timestamp = datetime.timestamp(datetime.now())
            
            thumb_ext = dest_thumb_image.filename.split('.')[::-1][0].lower()
            thumb_filename = "dest-thumb-{name}.{ext}".format(name=timestamp, ext=thumb_ext)
            thumb_image = app_config.UPLOAD_FOLDER + thumb_filename

            banner_ext = dest_banner_image.filename.split('.')[::-1][0].lower()
            banner_filename = "dest-banner-{name}.{ext}".format(name=timestamp, ext=banner_ext)
            banner_image = app_config.UPLOAD_FOLDER + banner_filename

            highlight_ext = dest_highlight_image.filename.split('.')[::-1][0].lower()
            highlight_filename = "dest-highlight-{name}.{ext}".format(name=timestamp, ext=highlight_ext)
            highlight_image = app_config.UPLOAD_FOLDER + highlight_filename

            activity_ext = dest_activity_image.filename.split('.')[::-1][0].lower()
            activity_filename = "dest-activity-{name}.{ext}".format(name=timestamp, ext=activity_ext)
            activity_image = app_config.UPLOAD_FOLDER + activity_filename
           
            try:
                destinationObj = Destinations(
                    dest_title = str(dest_title),
                    dest_description = dest_description,
                    dest_thumb_image = thumb_filename,
                    dest_banner_image = banner_filename,
                    dest_highlights = dest_highlights,
                    dest_highlight_image = highlight_filename,
                    dest_activities = dest_activities,
                    dest_activity_image = activity_filename,
                    dest_location_info = str(dest_location_info),
                    dest_language_info = str(dest_language_info),
                    dest_currency_info = str(dest_currency_info),
                    dest_cuisine_info = str(dest_cuisine_info),
                    dest_airport_info = str(dest_airport_info),
                    dest_flight_duration_info = str(dest_flight_duration_info),
                    dest_entered_date = datetime.now(),
                    dest_update_date = datetime.now()
                )

                db.session.add(destinationObj)
                db.session.commit()

                dest_thumb_image.save(thumb_image)
                dest_banner_image.save(banner_image)
                dest_highlight_image.save(highlight_image)
                dest_activity_image.save(activity_image)
                flash("Destination added successfully", category="success")
                return redirect(url_for('destinations.destination_list'))
            except:
                os.remove(thumb_image)
                os.remove(banner_image)
                os.remove(highlight_image)
                os.remove(activity_image)
                abort(400)

    return render_template('destination-add.html', postData=postData)

@mod_dest.route('/destination-edit/<int:dest_id>', methods=['POST', 'GET'])
@login_required
def destination_edit(dest_id):
    destination_row = Destinations.query.filter_by(iddestination = dest_id).first()
    postData = ""
    if (request.method == "POST" and request.form['btnsave'] == 'save'):
        postData = request.form
        dest_title = escape(postData['destination_title'])
        dest_description = request.form.get('destination_description')
        dest_thumb_image = request.files['destination_thumb_image']
        dest_hdnthumb_image = postData['hdndest_thumb_image']
        dest_banner_image = request.files['destination_banner_image']
        des_hdnbanner_image = postData['hdndest_banner_image']
        dest_highlights = request.form.get('destination_highlights')
        dest_highlight_image = request.files['destination_highlight_image']
        dest_hdnhighlight_img = postData['hdndest_highlight_image']
        dest_activities = request.form.get('destination_activities')
        dest_activity_image = request.files['destination_activity_image']
        dest_hdn_activity_image = postData['hdndest_activity_image']
        dest_location_info = escape(postData['dest_location_info'])
        dest_language_info = escape(postData['dest_language_info'])
        dest_currency_info = escape(postData['dest_currency_info'])
        dest_cuisine_info = escape(postData['dest_cuisine_info'])
        dest_airport_info = escape(postData['dest_airport_info'])
        dest_flight_duration_info = postData['dest_flight_duration_info']

        if dest_thumb_image.filename != '':
            os.remove(app_config.UPLOAD_FOLDER + destination_row.dest_thumb_image)
        if dest_banner_image.filename != '':
            os.remove(app_config.UPLOAD_FOLDER + destination_row.dest_banner_image)
        if dest_highlight_image.filename != '':
            os.remove(app_config.UPLOAD_FOLDER + destination_row.dest_highlight_image)
        if dest_activity_image.filename != '':
            os.remove(app_config.UPLOAD_FOLDER + destination_row.dest_activity_image)

        if (dest_title == ""):
            flash('Destination title should be mandatory', category="danger")
        elif (dest_description == ""):
            flash("Destination description should be mandatory", category="danger")
        elif (dest_thumb_image.filename == "" and dest_hdnthumb_image == ""):
            flash("Destination thumb image should be mandatory", category="danger")
        elif (dest_thumb_image.filename != "" and not allowed_filename(dest_thumb_image.filename)):
            flash('Uploaded thumb image extension not allowed', category="danger")
        elif (dest_banner_image.filename == "" and des_hdnbanner_image == ""):
            flash("Destination banner image should be mandatory", category="danger")
        elif (dest_banner_image.filename != "" and not allowed_file(dest_banner_image.filename)):
            flash('Uploaded banner image extension not allowed', category="danger")
        elif (dest_highlights == ""):
            flash("Destination highlights should be mandatory", category="danger")
        elif (dest_highlight_image.filename == "" and dest_hdnhighlight_img == ""):
            flash("Destination should be mandatory", category='danger')
        elif (dest_highlight_image.filename != "" and not allowed_file(dest_highlight_image.filename)):
            flash('Uploaded highlight image extension not allowed', category="danger")
        elif (dest_activities == ""):
            flash("Destination activities should be mandatory", category="danger")
        elif (dest_activity_image.filename == "" and dest_hdn_activity_image == ""):
            flash("Destination activities image should be mandatory", category="danger")
        elif (dest_activity_image.filename != "" and not allowed_file(dest_activity_image.filename)):
            flash('Uploaded acitivity image extension not allowed', category="danger")
        elif (dest_location_info == ""):
            flash("Destination location info should be mandatory", category="danger")
        elif (dest_language_info == ""):
            flash("Destination language info should be mandatory", category="danger")
        elif (dest_currency_info == ""):
            flash("Destination currency infor should be mandatory", category="danger")
        elif (dest_cuisine_info == ""):
            flash("Destination cuisine info should be mandatory", category="danger")
        elif (dest_airport_info == ""):
            flash("Destination airport infor should be mandatory", category="danger")
        elif (dest_flight_duration_info == ""):
            flash("Destination flight duration info should be mandatory", category="danger")
        else:
            try:
                if dest_thumb_image.filename != '':
                    timestamp = datetime.timestamp(datetime.now())
                    thumb_ext = dest_thumb_image.filename.split('.')[::-1][0].lower()
                    thumb_filename = "dest-thumb-{name}.{ext}".format(name=timestamp, ext=thumb_ext)
                    thumb_image = app_config.UPLOAD_FOLDER + thumb_filename
                    dest_thumb_image.save(thumb_image)
                else:
                    thumb_filename = str(dest_hdnthumb_image)
                
                if dest_banner_image.filename != '':
                    timestamp = datetime.timestamp(datetime.now())
                    banner_ext = dest_banner_image.filename.split('.')[::-1][0].lower()
                    banner_filename = "dest-banner-{name}.{ext}".format(name=timestamp, ext=banner_ext)
                    banner_image = app_config.UPLOAD_FOLDER + banner_filename
                    dest_banner_image.save(banner_image)
                else:
                    banner_filename = str(des_hdnbanner_image)
                
                if dest_highlight_image.filename != '':
                    timestamp = datetime.timestamp(datetime.now())
                    highlight_ext = dest_highlight_image.filename.split('.')[::-1][0].lower()
                    highlight_filename = "dest-banner-{name}.{ext}".format(name=timestamp, ext=highlight_ext)
                    highlight_image = app_config.UPLOAD_FOLDER + highlight_filename
                    dest_highlight_image.save(highlight_image)
                else:
                    highlight_filename = str(dest_hdnhighlight_img)

                if dest_activity_image.filename != '':
                    timestamp = datetime.timestamp(datetime.now())
                    activity_ext = dest_activity_image.filename.split('.')[::-1][0].lower()
                    activity_filename = "dest-banner-{name}.{ext}".format(name=timestamp, ext=activity_ext)
                    activity_image = app_config.UPLOAD_FOLDER + activity_filename
                    dest_activity_image.save(activity_image)
                else:
                    activity_filename = str(dest_hdn_activity_image)

                destination_row.dest_title = str(dest_title),
                destination_row.dest_description = dest_description,
                destination_row.dest_thumb_image = thumb_filename,
                destination_row.dest_banner_image = banner_filename,
                destination_row.dest_highlights = dest_highlights,
                destination_row.dest_highlight_image = highlight_filename,
                destination_row.dest_activities = dest_activities,
                destination_row.dest_activity_image = activity_filename,
                destination_row.dest_location_info = str(dest_location_info),
                destination_row.dest_language_info = str(dest_language_info),
                destination_row.dest_currency_info = str(dest_currency_info),
                destination_row.dest_cuisine_info = str(dest_cuisine_info),
                destination_row.dest_airport_info = str(dest_airport_info),
                destination_row.dest_flight_duration_info = str(dest_flight_duration_info)
                db.session.commit()
                flash('Destination updated successfully', category="success")
                return redirect(url_for('destinations.destination_list'))
            except:
                if dest_thumb_image.filename != '':
                    os.remove(app_config.UPLOAD_FOLDER + destination_row.dest_thumb_image)
                if dest_banner_image.filename != '':
                    os.remove(app_config.UPLOAD_FOLDER + destination_row.dest_banner_image)
                if dest_highlight_image.filename != '':
                    os.remove(app_config.UPLOAD_FOLDER + destination_row.dest_highlight_image)
                if dest_activity_image.filename != '':
                    os.remove(app_config.UPLOAD_FOLDER + destination_row.dest_activity_image)
                abort(400)

    return render_template('destination-edit.html', destination_row=destination_row, postData=postData)

@mod_dest.route('/destination-delete/<int:dest_id>', methods=['GET'])
@login_required
def destination_delete(dest_id):
    destination_data = Destinations.query.filter_by(iddestination = dest_id).first()
    dir = app_config.UPLOAD_FOLDER
    os.remove(dir + destination_data.dest_thumb_image)
    os.remove(dir + destination_data.dest_banner_image)
    os.remove(dir + destination_data.dest_highlight_image)
    os.remove(dir + destination_data.dest_activity_image)
    db.session.query(Destinations).filter_by(iddestination = dest_id).delete()
    db.session.commit()
    flash('Destination deleted successfully', category="danger")
    return redirect(url_for('destinations.destination_list'))

@mod_dest.route('/destination-image/<filename>', methods=['GET'])
@login_required
def show_image(filename):
    return redirect(url_for('static', filename='uploads/'+filename, code=301))

def allowed_filename(filename):
    return '.' in filename and \
        filename.split('.')[::-1][0].lower() in app_config.ALLOWED_EXTENSIONS