from app import db

class Packages(db.Model):
    __tablename__ = "packages"

    idpackage = db.Column(db.Integer, primary_key = True, nullable = False)
    package_name = db.Column(db.String(255), nullable= False)
    package_description = db.Column(db.Text(), nullable = False)
    package_thumb_image = db.Column(db.String(255), nullable = False)
    package_banner_image = db.Column(db.String(255), nullable = False)

    def __repr__(self) -> str:
        return 'Packaged ID: {}'.format(self.idpackage)

class PackageTrip(db.Model):
    __tablename__ = "packages_trip"

    idpackages_trip = db.Column(db.Integer, primary_key = True, nullable = False)
    idpackage = db.Column(db.Integer, nullable= False)
    idtrips = db.Column(db.Integer, nullable= False)

class PackagesDestination(db.Model):
    __tablename__ = "packages_destination"

    idpackages_dest = db.Column(db.Integer, primary_key = True, nullable = False)
    idpackage = db.Column(db.Integer, nullable= False)
    iddestination = db.Column(db.Integer, nullable= False)
