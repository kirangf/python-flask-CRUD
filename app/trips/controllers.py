from os import abort
from flask import Blueprint, request, render_template, url_for, redirect, flash, session, escape, abort
from flask_login import login_required
from flask_paginate import Pagination, get_page_parameter
from datetime import datetime
from config import app_config
from app.trips.models import Trips
from app import db
import os

mod_trip = Blueprint('trips', __name__, url_prefix='/admin', template_folder='templates')

@mod_trip.route('/trip-list/', methods=['POST', 'GET'])
@login_required
def trip_list():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    searchdata = ""
    if (request.method == 'POST' and request.form['btnsubmit'] == 'Search' and request.form['search_title'] != ''):
        searchdata = request.form['search_title']
        keyword = "%{}%".format(searchdata)
        tripObj = Trips.query.filter(
            (Trips.trip_name.like(keyword) | (Trips.trip_description.like(keyword))
            ))
        triplist = tripObj.all()
        total = tripObj.count()
    else:
        triplist = Trips.query.all()
        total = Trips.query.count()
    pagination = Pagination(page=page, per_page = app_config.PER_PAGE, total=total, search=False, record_name='trips')
    return render_template('tripslist.html', trip_list = triplist, datetime=datetime, pagination=pagination, searchpresist=searchdata)

@mod_trip.route('/add-trip/', methods=['POST', 'GET'])
@login_required
def add_trip():
    postData = {}
    if request.method == 'POST' and request.form['btnsave'] == 'save':
        postData            = request.form
        trip_title          = escape(postData['trip_title'])
        trip_description    = escape(request.form.get('ckeditor'))
        trip_thumb_image    = request.files['trip_thump_image']
        trip_banner_image   = request.files['trip_banner_image']
        if trip_title == "":
            flash('Trip title should be mandatroy', category="danger")
        elif trip_description == "":
            flash('Trip description should be mandatory', category="danger")
        elif trip_thumb_image.filename == '':
            flash('Thumb image should be mandatory', category="danger")
        elif trip_thumb_image and not allowed_file(trip_thumb_image.filename):
            flash('Uploaded thumb image extension not allowed', category="danger")
        elif trip_banner_image.filename == '':
            flash('Banner image should be mandatory', 'danger')
        elif trip_banner_image and not allowed_file(trip_banner_image.filename):
            flash("Uploaded banner image extension not allowed", "danger")
        else:
            timestamp = datetime.timestamp(datetime.now())
            thumext = trip_thumb_image.filename.split('.')[::-1][0].lower()
            thumbname = "trip-thumb-{uniquename}.{ext}".format(uniquename=timestamp, ext=thumext)
            thumbimage = app_config.UPLOAD_FOLDER + thumbname
            
            bannerext = trip_banner_image.filename.split('.')[::-1][0].lower()
            bannername = "trip-banner-{uniquename}.{ext}".format(uniquename=timestamp, ext=bannerext)
            bannerimage = app_config.UPLOAD_FOLDER + bannername
            
            try:
                tripObj = Trips(
                        trip_name = str(trip_title), 
                        trip_description = str(trip_description), 
                        trip_thumbimage = thumbname,
                        trip_bannerimage = bannername,
                        trip_entered_date = datetime.now(),
                        trip_update_date = datetime.now())
                trip_thumb_image.save(thumbimage)
                trip_banner_image.save(bannerimage)
                db.session.add(tripObj)
                db.session.commit()
            except:
                os.remove(bannerimage)
                os.remove(thumbimage)
                abort(400)
            
            flash('Trip inserted successfully', category="success")
            return redirect(url_for('trips.trip_list'))
            
    return render_template('addtrip.html', postData=postData)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.')[::-1][0].lower() in app_config.ALLOWED_EXTENSIONS

@mod_trip.route('/edit-trip/<int:tripid>', methods=['POST', 'GET'])
def edit_trip(tripid):
    trip_row = Trips.query.filter_by(idtrip = tripid).first()
    if trip_row is None:
        abort(404)

    if request.method == 'POST' and request.form['btnsave'] == 'save':
        postData            = request.form
        trip_title          = escape(postData['trip_title'])
        trip_description    = escape(request.form.get('ckeditor'))
        trip_thumb_image    = request.files['trip_thump_image']
        trip_hdn_thumb      = escape(postData['hdnthumbimage'])
        trip_banner_image   = request.files['trip_banner_image']
        trip_hdn_banner     = escape(postData['hdnbannerimage'])

        if trip_thumb_image.filename != '':
            os.remove(app_config.UPLOAD_FOLDER + trip_row.trip_thumbimage)
        if trip_banner_image.filename != '':
            os.remove(app_config.UPLOAD_FOLDER + trip_row.trip_bannerimage)

        if trip_title == "":
            flash('Trip title should be mandatroy', category="danger")
        elif trip_description == "":
            flash('Trip description should be mandatory', category="danger")
        elif trip_thumb_image.filename == '' and trip_hdn_thumb == '':
            flash('Thumb image should be mandatory', category="danger")
        elif trip_thumb_image and not allowed_file(trip_thumb_image.filename):
            flash('Uploaded thumb image extension not allowed', category="danger")
        elif trip_banner_image.filename == '' and trip_hdn_banner == '':
            flash('Banner image should be mandatory', 'danger')
        elif trip_banner_image and not allowed_file(trip_banner_image.filename):
            flash("Uploaded banner image extension not allowed", "danger")
        else:
            if trip_thumb_image.filename != '':
                # os.remove(app_config.UPLOAD_FOLDER + trip_row.trip_thumbimage)
                timestamp = datetime.timestamp(datetime.now())
                thumext = trip_thumb_image.filename.split('.')[::-1][0].lower()
                thumbname = "trip-thumb-{uniquename}.{ext}".format(uniquename=timestamp, ext=thumext)
                thumbimage = app_config.UPLOAD_FOLDER + thumbname
                trip_thumb_image.save(thumbimage)
            else:
                thumbname = str(trip_hdn_thumb)

            if trip_banner_image.filename != '':
                # os.remove(app_config.UPLOAD_FOLDER + trip_row.trip_bannerimage)
                timestamp = datetime.timestamp(datetime.now())
                bannerext = trip_banner_image.filename.split('.')[::-1][0].lower()
                bannername = "trip-banner-{uniquename}.{ext}".format(uniquename=timestamp, ext=bannerext)
                bannerimage = app_config.UPLOAD_FOLDER + bannername
                trip_banner_image.save(bannerimage)
            else:
                bannername = str(trip_hdn_banner)
            
            try:
                trip_data = Trips.query.filter_by(idtrip = tripid).first()
                trip_data.trip_name = str(trip_title)
                trip_data.trip_description = str(trip_description)
                trip_data.trip_thumbimage = str(thumbname)
                trip_data.trip_bannerimage = str(bannername)
                db.session.commit()
                flash('Trip updated successfully', 'success')
                return redirect(url_for('trips.trip_list'))
            except:
                if trip_banner_image.filename != '':
                    os.remove(bannerimage)
                if trip_thumb_image.filename != '':
                    os.remove(thumbimage)
                abort(400)

    return render_template('edittrip.html', triprow = trip_row)

@mod_trip.route('/display-tripimage/<filename>')
def display_tripimage(filename):
    return redirect(url_for('static', filename='uploads/'+filename), code=301)

@mod_trip.route('/delete-trip/<int:tripid>', methods=["GET"])
def delete_trip(tripid):
    trip_data = Trips.query.filter_by(idtrip = tripid).first()
    os.remove(app_config.UPLOAD_FOLDER + trip_data.trip_thumbimage)
    os.remove(app_config.UPLOAD_FOLDER + trip_data.trip_bannerimage)
    db.session.query(Trips).filter_by(idtrip = tripid).delete()
    db.session.commit()
    flash('Trip deleted successfully', "success")
    return redirect(url_for('trips.trip_list'))