from app import app
from app.auth.controllers import mod_auth as auth_module
from app.dashboard.controllers import mod_dashboard as dashboard_module
from app.trips.controllers import mod_trip as trip_module
from app.destinations.controllers import mod_dest as destination_module
from app.packages.controllers import mod_packages as packages_modules

app.register_blueprint(auth_module)
app.register_blueprint(dashboard_module)
app.register_blueprint(trip_module)
app.register_blueprint(destination_module)
app.register_blueprint(packages_modules)