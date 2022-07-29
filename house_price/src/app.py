import os

from flask import Flask, send_from_directory

import logging
logger = logging.getLogger(__name__)

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
    logger.info('Home route called.')
    return 'Machine learning project.'