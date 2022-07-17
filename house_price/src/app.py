import os

from flask import Flask, send_from_directory

from house_price.logger import logging

app = Flask(__name__)

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.route('/')
def home():
    logging.info('Home route called.')
    return 'Machine learning project.'