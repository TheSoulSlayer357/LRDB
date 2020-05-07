from flask import render_template, url_for, flash, redirect, request,session, send_file
from LRDB.models import fm_profiles,land_details,land_requests, transactions
from . import bc_settings as block
from io import BytesIO
import hashlib
from LRDB import db,app
import random
import mysql.connector
conn = mysql.connector.connect(host="localhost",user="root",passwd="root", database="lrdb")

@app.route("/")
def index():
    return render_template("home.html")

@app.route('/register', methods = ['GET', 'POST'])
def usr_reg():
    if request.method=='POST':
        try:
            fname = request.form['first_name']
            lname = request.form['last_name']
            email = request.form['email']
            pswd = request.form['password']
            id = request.form['unique_id']

            register = fm_profiles(id=id,fname=fname,lname=lname,email=email,pswd=pswd)
            db.session.add(register)
            db.session.commit()
            flash('Successful Registration')
            return redirect('/login')
        except: 
            flash('Error in registering. Please try again later')
    return render_template('register.html')

@app.route('/login', methods = ['GET','POST'])
def usr_log():
    if request.method=='POST':
        mail = request.form['email']
        pswd = request.form['password']

        login = fm_profiles.query.filter_by(email=mail, pswd=pswd).first()
        if login is not None:
            session['fname'] = login.fname
            session['lname'] = login.lname
            session['id'] = login.id
            return redirect('/profile')
        else:
            flash('Login failed. Check credentials and try again')
    return render_template('login.html')

@app.route('/profile/<fno>', methods=['GET','POST'])
@app.route('/profile/', methods=['GET','POST'])
def profile(fno=None):
    profile = fm_profiles.query.filter_by(id=session['id']).first()
    if fno=='1':
        if request.method == 'POST':
            fname=request.form['first_name']
            lname=request.form['last_name']
            uname=request.form['username']
            email=request.form['email']
            profile.lname = lname
            profile.email = email
            profile.username = uname
            db.session.commit()
    else:
        if request.method=='POST':
            addr = request.form['address']
            city = request.form['city']
            country = request.form['country']
            profile.addr = addr
            profile.city = city
            profile.country = country
            db.session.commit()
    return render_template('profile.html',name = session['fname']+' '+session['lname'], data = profile)

@app.route('/land-register', methods=['GET', 'POST'])
def land_reg():
    f1_hash = hashlib.sha256() #set the hashing algo  
    f2_hash = hashlib.sha256() #set the hashing algo  
    f3_hash = hashlib.sha256() #set the hashing algo  
    f4_hash = hashlib.sha256() #set the hashing algo  
    if request.method == 'POST': #Check for POST method for form 
        # try:
            f1 = request.files["doc1"].read()
            f2 = request.files["doc2"].read()
            f3 = request.files["doc3"].read()
            f4 = request.files["doc4"].read()
            f1_hash.update(f1)
            f2_hash.update(f2)
            f3_hash.update(f3)
            f4_hash.update(f4)
            doc1_hash = f1_hash.hexdigest()
            doc2_hash = f2_hash.hexdigest()
            doc3_hash = f3_hash.hexdigest()
            doc4_hash = f4_hash.hexdigest()
            register_land = land_details(id=request.form['uid'],fname=session['fname'], lname=session['lname'],doc1=f1,doc2=f2,doc3=f3,doc4=f4,land_id=random.randint(1,1000),sell=0,size=request.form['size'],price=0,loc=request.form['loc'])
            db.session.add(register_land)
            tx_hash = block.contract.functions.setFarmer(int(request.form['uid']),session['fname'],session['lname'],doc1_hash,doc2_hash,doc3_hash,doc4_hash).transact() #Blockchain Function code
            tx_receipt = block.w3.eth.waitForTransactionReceipt(tx_hash)
            transact = transactions(t_id = tx_receipt.blockNumber, transaction_id = tx_hash.hex(), use_case= "Land Registration")
            db.session.add(transact)
            db.session.commit()
            flash('Land Registered Successsfully')
            return redirect('/profile')
        # except:
        #     flash('Land Registration Unsuccessful. Check details before entering')            
    return render_template('land-register.html',name=session['fname']+' '+session['lname'])    


@app.route('/table')
def table():
    land = land_details.query.filter_by(id=session['id']).all()
    print('Contract Information : {}'.format(block.contract.functions.getFarmer(int(session['id'])).call()))
    return render_template('table.html',data=land, name=session['fname']+' '+session['lname'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/download/<land_id>/<doc>', methods=['GET','POST'])
def download(land_id,doc):
    land = land_details.query.filter_by(land_id=land_id).first()

    if doc=='doc1':
        data = land.doc1
        return send_file(BytesIO(data),attachment_filename='flask.txt',as_attachment=True)
    elif doc=='doc2':
        data = land.doc2
        return send_file(BytesIO(data),attachment_filename='flask.txt',as_attachment=True)
    elif doc=='doc3':
        data = land.doc3
        return send_file(BytesIO(data),attachment_filename='flask.txt',as_attachment=True)
    elif doc=='doc4':
        data = land.doc4
        return send_file(BytesIO(data),attachment_filename='flask.txt',as_attachment=True)

@app.route('/sell_market/<land_id>/<price>', methods=['GET','POST'])
def sell_market(land_id, price):
    try:
        land = land_details.query.filter_by(land_id=land_id).first()
        land.sell = 1
        land.price = price
        db.session.commit()
        flash('Land is set to sell')
    except:
        flash('Land not set to sell. Please try again later')
    return redirect('/table')

@app.route('/marketplace')
def marketplace():
    land_sell = land_details.query.filter_by(sell=1)
    return render_template('marketplace.html',data = land_sell,name=session['fname']+' '+session['lname'])

@app.route('/requests/<land_id>/<uid>/<to_user>', methods=['GET','POST'])
def requests(land_id,uid,to_user):
    try:
        from_user = session['fname']
        from_user_id = session['id']
        to_user_id = uid
        req = land_requests(Land_ID = land_id, To_user = to_user, From_user = from_user, status=0, to_user_id = to_user_id, from_user_id = from_user_id)
        db.session.add(req)
        db.session.commit()
        flash('Request sent','warnings')
    except:
        flash('Request not sent','warnings')
    return redirect('/marketplace')

@app.route('/checkreq')
def checkreq():
    req = land_requests.query.filter_by(to_user_id = session['id'])
    return render_template('check_req.html',data=req)

@app.route('/setstatus/<land_id>/<from_user_id>/<status>')
def setstatus(land_id,from_user_id,status):
    if status == '1':
        f1_hash = hashlib.sha256() #set the hashing algo  
        f2_hash = hashlib.sha256() #set the hashing algo  
        f3_hash = hashlib.sha256() #set the hashing algo  
        f4_hash = hashlib.sha256() #set the hashing algo  

        user = fm_profiles.query.filter_by(id=from_user_id).first()
        land = land_details.query.filter_by(land_id=land_id).first()

        f1 = land.doc1
        f2 = land.doc2
        f3 = land.doc3
        f4 = land.doc4
        f1_hash.update(f1)
        f2_hash.update(f2)
        f3_hash.update(f3)
        f4_hash.update(f4)
        do1_hash = f1_hash.hexdigest()
        do2_hash = f2_hash.hexdigest()
        do3_hash = f3_hash.hexdigest()
        do4_hash = f4_hash.hexdigest()

        land.id = user.id
        land.fname = user.fname
        land.lname = user.lname
        land.sell=0
        land.price=0
        db.session.commit()
        req = land_requests.query.filter_by(Land_ID=land_id).first()
        db.session.delete(req)
        db.session.commit()

        tx_hash = block.contract.functions.setFarmer(int(user.id),user.fname,user.lname,do1_hash,do2_hash,do3_hash,do4_hash).transact() #Blockchain Function code 
        tx_receipt = block.w3.eth.waitForTransactionReceipt(tx_hash)
        transact = transactions(t_id = tx_receipt.blockNumber, transaction_id = tx_hash.hex(), use_case= "Land Updated from "+session['fname']+" to "+user.fname)
        db.session.add(transact)
        db.session.commit()
        print('Request has been accepted. Transaction successsfull')
    elif status == '0':
        req = land_requests.query.filter_by(Land_ID=land_id).first()
        db.session.delete(req)
        db.session.commit()
        # ack = db_meths.request_handler(status,land_id,from_user_id)
        print('Request has been declined')
    return redirect('/profile')


@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method=='POST':
        mail = request.form['email']
        pswd = request.form['password']
        login = fm_profiles.query.filter_by(email=mail, pswd=pswd, admin='1').first()
        if login is not None:
            session['admin_fname'] = login.fname
            session['admin_lname'] = login.lname
            return redirect('/admin_profile')
        else:
            flash('Login failed. Check credentials or contact administrator and try again')     
    return render_template('admin_login.html')

@app.route('/admin_profile/<option>')
@app.route('/admin_profile')
def admin_prof(option=None):
    if option=="land_tb":
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM land_details")
        prof_data = cursor.fetchall()
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'land_details' order by ordinal_position asc")
        prof_col = cursor.fetchall()
        return render_template('admin_profile.html', data = prof_data, name=session['admin_fname']+' '+session['admin_lname'], col = prof_col)
    elif option=="profile_tb":
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fm_profiles")
        prof_data = cursor.fetchall()
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'fm_profiles' order by ordinal_position asc")
        prof_col = cursor.fetchall()
        for i in prof_col:
            print(i[0])
        return render_template('admin_profile.html', data = prof_data, name=session['admin_fname']+' '+session['admin_lname'], col = prof_col)
    elif option=="transactions":
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions")
        prof_data = cursor.fetchall()
        cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'transactions' order by ordinal_position asc")
        prof_col = cursor.fetchall()
        return render_template('admin_profile.html', data = prof_data, name=session['admin_fname']+' '+session['admin_lname'], col = prof_col)
    return render_template('admin_profile.html' ,name=session['admin_fname']+' '+session['admin_lname'])

