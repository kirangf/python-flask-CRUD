from app import db

class Destinations(db.Model):
    __tablename__ = 'destinations'

    iddestination = db.Column(db.Integer, primary_key = True)
    dest_title = db.Column(db.String(255), nullable = False)
    dest_description = db.Column(db.Text(), nullable = False)
    dest_thumb_image = db.Column(db.String(255), nullable = False)
    dest_banner_image = db.Column(db.String(255), nullable = False)
    dest_highlights = db.Column(db.Text(), nullable = False)
    dest_highlight_image = db.Column(db.String(255), nullable = False)
    dest_activities = db.Column(db.Text(), nullable = False)
    dest_activity_image= db.Column(db.String(255), nullable = False)
    dest_location_info = db.Column(db.String(100), nullable = False)
    dest_language_info = db.Column(db.String(100), nullable = False)
    dest_currency_info = db.Column(db.String(100), nullable = False)
    dest_cuisine_info = db.Column(db.String(100), nullable= False)
    dest_airport_info = db.Column(db.String(100), nullable = False)
    dest_flight_duration_info = db.Column(db.String(100), nullable = False)
    dest_entered_date = db.Column(db.DateTime, default = db.func.current_timestamp())
    dest_update_date = db.Column(
                            db.DateTime,
                            default = db.func.current_timestamp(),
                            onupdate = db.func.current_timestamp())
    
    def __repr__(self):
        return 'Destination ID: {}'.format(self.iddestination)
