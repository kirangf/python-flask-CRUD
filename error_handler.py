from flask import render_template
from app import app

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error_pages/404.html')

@app.errorhandler(400)
def bad_request(error):
    print(error)
    print('******************')
    return render_template('error_pages/400.html')

@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('error_pages/405.html')