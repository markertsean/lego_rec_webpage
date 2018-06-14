from flask import render_template
from flaskexample import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
import psycopg2

from flask import request
from a_Model import ModelIt

# Imports from shelfy
import os
import sys
import flask
from werkzeug.utils import secure_filename
#import book_functions, scraper, server, utility





user = 'postgres' #add your username here (same as previous postgreSQL)                      
pwd  = 'postgres'
host = 'localhost'
dbname = 'birth_db'
db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
con = None
con = psycopg2.connect(database = dbname, user = user, password = pwd, host=host, )

_project_title = 'Lego Set Recommender'

# Define views
#views = flask.Blueprint('views', __name__)

UPLOAD_FOLDER = '/home/sean/Insight/web_demo/uploaded_images/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


#@app.route('/')
#@app.route('/index')
#def index():
#    return render_template("index.html",
#       title = _project_title,

#       )


#import main
#sys.path.append(main.SHELFY_BASE_PATH + '/models')




@app.route('/', methods=['GET', 'POST'])
def index():
    '''
    The index; a simple interface for allowing a user to submit an image
    to query
    methods:
        GET: The main page, has a 'submit image' button
        POST: After the submit/query/request button is hit, the file will be saved
        to the server and the user will be redirected to the uploads page
    '''


    # Get method type
    method = flask.request.method


    if method == 'GET':
        return flask.render_template('index.html')
    
    if method == 'POST':

        
        # No file found in the POST submission
        if 'file' not in flask.request.files:
            return flask.redirect(flask.request.url)

        # File was found
        my_file = flask.request.files['file']

        # No file name submitted
        if my_file.filename == '':
            return flask.redirect(request.url)

        # File was found, and is an allowable file type
        if my_file:
            print 'fuck'
            # Create a new submission folder for the submission
#            submission_id = server.create_new_submission(my_file)

            # Full pipeline
#            raw_file_path = server.get_raw_image_path_from_submission_id(submission_id)
#            books = utility.full_pipeline(raw_file_path)


            # Save the processed image
#            proc_file_path = server.get_processed_image_path_from_submission_id(submission_id)
#            book_functions.generate_processed_image(books, raw_file_path, save_path = proc_file_path)

            # Pickle and save the books
#            server.pickle_save_books(books, submission_id)

            # Save json of book info
#            server.save_book_info(books, submission_id)



#            return flask.redirect('/submission/' + submission_id + '/user')
            return flask.redirect('/')