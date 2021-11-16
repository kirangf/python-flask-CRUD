from os import abort
from flask import Blueprint, request, redirect, url_for, flash, render_template, escape
from flask_login import login_required
from flask_paginate import Pagination, get_page_parameter
from app.packages.models import Packages, PackageTrip, PackagesDestination
from app.trips.models import Trips
from app.destinations.models import Destinations
from datetime import datetime
from config import app_config
from app import db

mod_packages = Blueprint('packages', __name__, url_prefix='/admin', template_folder="templates")

@mod_packages.route('/packages-list', methods=['GET', 'POST'])
@login_required
def packages_list():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    searchdata = ""
    destinations = Destinations.query.all()
    trips = Trips.query.all()
    if request.method == "POST" and request.form['btnsubmit'] == 'Search':
        searchdata = request.form
        package_list = db.session.query(
            Packages.idpackage,
            Packages.package_name,
            db.func.group_concat(Trips.trip_name.distinct()).label('trip_name'),
            db.func.group_concat(Destinations.dest_title.distinct()).label('dest_title')
        ) \
        .join(PackageTrip, Packages.idpackage==PackageTrip.idpackage) \
        .join(Trips, PackageTrip.idtrips==Trips.idtrip) \
        .join(PackagesDestination, Packages.idpackage==PackagesDestination.idpackage) \
        .join(Destinations, PackagesDestination.iddestination==Destinations.iddestination) \
        .group_by(Packages.idpackage) \
        .order_by(Packages.idpackage.desc())
        if searchdata['search_title'] != "":
            keyword = "%{}%".format(searchdata['search_title'])
            package_list = package_list.filter(
                (Packages.package_name.like(keyword) | Packages.package_description.like(keyword))
            )
        if searchdata['package_trip'] != "":
            package_list = package_list.filter(PackageTrip.idtrips==int(searchdata['package_trip']))
        if searchdata['package_destination'] != "":
           package_list = package_list.filter(PackagesDestination.iddestination == int(searchdata['package_destination']))

        total = package_list.count()
    else:
        package_list = db.session.query(
            Packages.idpackage,
            Packages.package_name,
            db.func.group_concat(Trips.trip_name.distinct()).label('trip_name'),
            db.func.group_concat(Destinations.dest_title.distinct()).label('dest_title')
        ) \
        .join(PackageTrip, Packages.idpackage==PackageTrip.idpackage) \
        .join(Trips, PackageTrip.idtrips==Trips.idtrip) \
        .join(PackagesDestination, Packages.idpackage==PackagesDestination.idpackage) \
        .join(Destinations, PackagesDestination.iddestination==Destinations.iddestination) \
        .group_by(Packages.idpackage) \
        .order_by(Packages.idpackage.desc())
        total = package_list.count()
        
    pagination = Pagination(page=page, per_page = app_config.PER_PAGE, total=total, search=False, record_name='packages')
    return render_template('packages-list.html', destinations=destinations, trips=trips, package_list=package_list, datetime=datetime, pagination=pagination, searchpresist=searchdata)

@mod_packages.route('/packages-add', methods=['POST', 'GET'])
@login_required
def packages_add():
    postData = ""
    trips = Trips.query.all()
    destinations = Destinations.query.all()
    if (request.method == "POST" and request.form['btnsave'] == 'save'):
        postData = request.form
        package_name = escape(postData['package_name'])
        package_description = request.form.get('package_description')
        package_thumb_image = request.files['package_thumb_image']
        package_banner_image = request.files['package_banner_image']
        package_destination = postData.getlist('package_destination')
        package_trip = postData.getlist('package_trip')

        if (package_name == ""):
            flash('Package name should be mandatory', category="danger")
        elif (package_description == ""):
            flash("Package description should be mandatory", category="danger")
        elif (package_thumb_image.filename == ""):
            flash("Package thumb image should be mandatory", category="danger")
        elif (package_banner_image.filename == ""):
            flash("Package banner should be mandatory", category="danger")
        elif (package_destination == ""):
            flash("Package destination should be mandatory", category="danger")
        elif (package_trip == ""):
            flash("Package trip should be mandatory", category="danger")
        else:
            try:
                pkg_obj = Packages(
                    package_name = str(package_name),
                    package_description = package_description,
                    package_thumb_image = package_thumb_image.filename,
                    package_banner_image = package_banner_image.filename
                )
                db.session.add(pkg_obj)
                db.session.commit()

                lastID = pkg_obj.idpackage
 
                if package_destination is not None:
                    for x in package_destination:
                        p1 = PackagesDestination()
                        p1.idpackage = lastID
                        p1.iddestination = int(x)
                        db.session.add(p1)
                        db.session.flush()
                db.session.commit()

                if package_trip is not None:
                    for y in package_trip:
                        pkg_trip_obj = PackageTrip(
                            idpackage = lastID,
                            idtrips = int(y)
                        )
                        db.session.add(pkg_trip_obj)
                        db.session.flush()
                db.session.commit()

                flash("Package added successfully", category="success")
                redirect(url_for('packages.packages_list'))
            except:
                abort(400)


        

    return render_template('packages-add.html', trips=trips, destinations=destinations, postData=postData)

@mod_packages.route('/packages-edit/<int:package_id>', methods=['GET', 'POST'])
@login_required
def packages_edit(package_id):
    return render_template("packages-edit.html")

@mod_packages.route('/packages-delete/<int:package_id>', methods=['GET'])
@login_required
def package_delete(package_id):
    flash('Packages deleted successfully', category="success")
    return redirect(url_for('packages.packages_list'))
