from app import db

class Trips(db.Model):
    __tablename__ = 'trips'

    idtrip = db.Column(db.Integer, primary_key = True)
    trip_name = db.Column(db.String(255), nullable = False)
    trip_description = db.Column(db.Text(), nullable = False)
    trip_thumbimage = db.Column(db.String(255), nullable= False)
    trip_bannerimage = db.Column(db.String(255), nullable = False)
    trip_entered_date = db.Column(db.DateTime, default = db.func.current_timestamp())
    trip_update_date = db.Column(
                            db.DateTime, 
                            default = db.func.curent_timestamp(), 
                            onupdate = db.func.current_timestamp())
    
    def __repr__(self):
        return '<Trip {}>'.format(self.idtrip)