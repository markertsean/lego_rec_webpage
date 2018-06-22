import os
import sys

# Imports from shelfy
import flask
from flask import request
from flask import render_template
from flaskexample import app
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2


from werkzeug.utils import secure_filename


import PIL.Image as Image

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


#import book_functions, scraper, server, utility

sys.path.append('/home/sean/Insight/legos/tensorbox/')
import pred_location as pl

sys.path.append('/home/sean/Insight/legos/classification/')
import predict_lego_class as plc

######################## EDIT THIS LATER
user = 'postgres' #add your username here (same as previous postgreSQL)                      
pwd  = 'postgres'
host = 'localhost'
dbname = 'birth_db'
#db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
#con = None
#con = psycopg2.connect(database = dbname, user = user, password = pwd, host=host, )

_project_title = 'Lego Set Recommender'

# Define views
#views = flask.Blueprint('views', __name__)

UPLOAD_FOLDER = '/home/sean/Insight/web_demo/flaskexample/static/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


_SUMMARY_STR = ''

_OUT_FILE_NAME = 'out_img.jpg'
# 
def gen_img( inp_img ):
    global _OUT_FILE_NAME
    
    full_img_path = os.path.join( UPLOAD_FOLDER, 'in_img.jpg')
    
    inp_img.save( full_img_path )
        
    box_dict = pl.pred_lego_locations( full_img_path )

    lego_img = Image.open( full_img_path )

    fig, ax = plt.subplots(1)
    ax.imshow( lego_img )

    x_size = lego_img.size[0]
    y_size = lego_img.size[1]

    for box in box_dict:
        rect = Rectangle( ( box['x1']*x_size/640., box['y1']*y_size/480. ), 
                         (box['x2']-box['x1'])*x_size/640., 
                         (box['y2']-box['y1'])*y_size/480, linewidth=1,edgecolor='r',facecolor='None' )
        ax.add_patch(rect)

    ax.axis('off')
    for i in range( 0, 100 ):
        
        file_name = os.path.join(UPLOAD_FOLDER,'out_img_'+str(i)+'.jpg')
        if not os.path.isfile(file_name):
            break
    plt.savefig( os.path.join(UPLOAD_FOLDER,file_name) )
    _OUT_FILE_NAME = '/static/out_img_'+str(i)+'.jpg'

@app.after_request
def add_header(response):
    response.cache_control.max_age = 0
    return response





#import main
#sys.path.append(main.SHELFY_BASE_PATH + '/models')
@app.route('/show_result')
def show_img():
    print _OUT_FILE_NAME
    return render_template("display_box.html", img_file=_OUT_FILE_NAME, title='Results',result_str=_SUMMARY_STR )



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
    global _SUMMARY_STR

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
            
            # Generates the bounding box image
            gen_img( my_file )
            
            full_img_path = os.path.join( UPLOAD_FOLDER, 'in_img.jpg')

            # Get the classifications
            clf_list = plc.generate_prediction_string(full_img_path)
            
            print clf_list
            
            count_dict = {}
            total_sum  = 0
            
            for clf in clf_list:
                total_sum = total_sum + 1
                if (clf in count_dict.keys()):
                    count_dict[clf] = count_dict[clf] + 1
                else:
                    count_dict[clf] = 1
            
            _SUMMARY_STR = 'Total number of Legos detected: %i      ' % total_sum
            for key in count_dict.keys():
                _SUMMARY_STR = _SUMMARY_STR + '     %2i %s blocks,' % (count_dict[key],key)
            
#            return flask.redirect('/submission/' + submission_id + '/user')
            return flask.redirect('/show_result')