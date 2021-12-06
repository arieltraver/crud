# Ariel Traver and Jennifer Shan
# app.py

from os import fwalk
from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from pymysql import NULL
from werkzeug.utils import secure_filename
app = Flask(__name__)

# one or the other of these. Defaults to MySQL (PyMySQL)
# change comment characters to switch to SQLite

import cs304dbi as dbi
# import cs304dbi_sqlite3 as dbi
import crud
import random

app.secret_key = 'cs304'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

jid = int(8343)

@app.route('/')
def index():
    return render_template('main.html', page_title = 'Welcome')

@app.route('/insert/', methods=['GET','POST'])
def insert():
    if request.method == 'GET':
        return render_template('insert.html', page_title = 'Insert')
    else:
        tt = request.form.get('movie-tt')
        title = request.form.get('movie-title')
        release = request.form.get('movie-release')
        #sanitizing inputs
        if not tt or not title or not release:
            flash('missing input')
        else:
            try:
                int(tt)
            except:
                flash('tt must be an integer')
                return redirect(url_for('insert'))        
            if len(release) > 4:
                flash('date format: yyyy')
                return redirect(url_for('insert'))
            conn = dbi.connect()
            if len(crud.check_tt(conn, tt)) == 0:
                flash('tt does not already exist')
                crud.insert_mov(conn, tt, title, release, jid)
                session['title'] = title
                session['release'] = release
                return redirect(url_for('update', tt = tt))
            else: flash('tt already exists')
    return redirect(url_for('insert'))

@app.route('/update/<int:tt>', methods=['GET','POST'])
def update(tt):
    if request.method == 'GET':
        title = session.get('title')
        release = session.get('release')
        if session.get('director'):
            director = session.get('director')
        else:
            director = None
        if session.get('addedby'):
            addedby = session.get('addedby')
        else:
            addedby = jid
        return render_template('update.html', page_title = 'Update', tt = tt, title = title, release = release, director = director, addedby = addedby)
    else:
        newtt = request.form.get('movie-tt')
        conn = dbi.connect()
        if request.form.get('submit') == 'update':
            title = request.form.get('movie-title')
            release = request.form.get('movie-release')
            director = request.form.get('movie-director')
            addedby = request.form.get('movie-addedby')
            if int(newtt) != int(tt) and len(crud.check_tt(conn, newtt)) != 0:
                flash('tt already exists')
                return redirect(url_for('update', tt = tt))
            else:
                crud.update_mov(conn, tt, newtt, title, release, director, addedby)
                flash('movie updated successfully')
                return render_template('update.html', tt = newtt, title = title, release = release, director = director, addedby = addedby)
        elif request.form.get('submit') == 'delete':
            crud.delete_mov(conn, newtt)
            flash('movie was deleted successfully')
            return redirect(url_for('index')) 

@app.route('/select/', methods=['GET','POST'])
def select():
    if request.method == 'GET':
        conn = dbi.connect()
        movs = crud.select_mov(conn)
        return render_template('select.html', page_title = 'Select', movs = movs)
    else:
        tt = int(request.form.get('menu-tt'))
        conn = dbi.connect()
        info = crud.check_tt(conn, tt)[0]
        session['title'] = info['title']
        session['release'] = info['release']
        session['director'] = info['director']
        session['addedby'] = info['addedby']
        return redirect(url_for('update', tt = tt)) 

@app.before_first_request
def init_db():
    dbi.cache_cnf()
    # set this local variable to 'wmdb' or your personal or team db
    db_to_use = 'j8_db' 
    dbi.use(db_to_use)
    print('will connect to {}'.format(db_to_use))

if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)
