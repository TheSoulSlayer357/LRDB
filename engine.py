from flask import Flask, request, render_template, send_file, redirect,url_for, flash,session
import hashlib
import db_meths
import bc_settings
from io import BytesIO

app = Flask(__name__)
app.secret_key='hello mellow jello'

@app.route('/register', methods = ['GET', 'POST'])
def usr_reg():
    if request.method=='POST':
        ack = db_meths.set_prof(request.form['first_name'],request.form['last_name'],request.form['email'],request.form['password'],request.form['unique_id'])
        if ack==1:
            flash('Successful Registration') 
        else: 
            flash('Error in registering. Please try again later')
    return render_template('register.html')# /template/home.html

@app.route('/login', methods = ['GET','POST'])
def usr_log():
    if request.method=='POST':
        record=db_meths.get_prof(request.form['email'],request.form['password'])
        session['record_prof'] = record
        if record != 0:
            return redirect('/profile')
        else:
            flash('Login failed. Check credentials and try again')
            print('Login failed')
    return render_template('login.html')

@app.route('/profile')
def profile():
    return render_template('profile.html',data = session['record_prof'])

@app.route('/land-register', methods=['GET', 'POST'])
def land_reg():
    f1_hash = hashlib.sha256() #set the hashing algo  
    f2_hash = hashlib.sha256() #set the hashing algo  
    f3_hash = hashlib.sha256() #set the hashing algo  
    f4_hash = hashlib.sha256() #set the hashing algo  
    record = session['record_prof']
    if request.method == 'POST': #Check for POST method for form 
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
        ack = db_meths.set_land(record[4], record[0], record[1], f1, f2, f3, f4, request.form['loc'], request.form['size']) #Inserting data onto the database
        if ack == 1:
            bc_settings.contract.functions.setFarmer(int(record[4]),record[0],record[1],doc1_hash,doc2_hash,doc3_hash,doc4_hash).transact() #Blockchain Function code
            flash('Land Registered Successsfully')
        else:
            flash('Land Registration Unsuccessful. Check details before entering')
    return render_template('land-register.html')    


@app.route('/table')
def table():
    record_prof = session['record_prof']
    record_land = db_meths.get_land(record_prof[4])
    print('Contract Information : {}'.format(
        bc_settings.contract.functions.getFarmer(record_prof[4]).call()))
    return render_template('table.html',data=record_land, name=session['record_prof'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/download/<land_id>/<num>', methods=['GET','POST'])
def download(land_id,num):
    record_prof = session['record_prof']
    record_land = db_meths.get_land_uid(record_prof[4],land_id)
    data = record_land[int(num)]
    return send_file(BytesIO(data),attachment_filename='flask.txt',as_attachment=True)


@app.route('/sell_market/<land_id>/<price>', methods=['GET','POST'])
def sell_market(land_id, price):
    record = db_meths.sell_land(land_id,price)
    print(record)
    if record == 1:
        print('Land is set to sell')
    else:
        print('Land not set to sell. Please try again later')
    return redirect('/profile')
    
@app.route('/marketplace')
def marketplace():
    data = db_meths.get_land_sell()
    return render_template('marketplace.html',data = data,name=session['record_prof'])

@app.route('/requests/<land_id>/<uid>/<to_user>', methods=['GET','POST'])
def requests(land_id,uid,to_user):
    record_prof = session['record_prof']
    from_user = record_prof[0]
    from_user_id = record_prof[4]
    to_user_id = uid
    ack = db_meths.set_requests(land_id,to_user,from_user,to_user_id,from_user_id)
    if ack==1:
        flash('Request sent','warnings')
    else:
        flash('Request not sent','warnings')
    return redirect('/marketplace')

@app.route('/checkreq')
def checkreq():
    record_prof = session['record_prof']
    data = db_meths.get_requests(record_prof[0])
    return render_template('check_req.html',data=data)

@app.route('/setstatus/<land_id>/<from_user_id>/<status>')
def setstatus(land_id,from_user_id,status):
    if status == '1':
        f1_hash = hashlib.sha256() #set the hashing algo  
        f2_hash = hashlib.sha256() #set the hashing algo  
        f3_hash = hashlib.sha256() #set the hashing algo  
        f4_hash = hashlib.sha256() #set the hashing algo  
        record_prof = db_meths.get_prof_id(from_user_id)
        record_prof_to = session['record_prof']
        rec = db_meths.get_land_uid(record_prof_to[4],land_id)
        f1 = rec[3]
        f2 = rec[4]
        f3 = rec[5]
        f4 = rec[6]
        uid = record_prof[4]
        fname = record_prof[0]
        lname = record_prof[1]
        f1_hash.update(f1)
        f2_hash.update(f2)
        f3_hash.update(f3)
        f4_hash.update(f4)
        do1_hash = f1_hash.hexdigest()
        do2_hash = f2_hash.hexdigest()
        do3_hash = f3_hash.hexdigest()
        do4_hash = f4_hash.hexdigest()
        ack = db_meths.request_handler(status,land_id,from_user_id)
        bc_settings.contract.functions.setFarmer(uid,fname,lname,do1_hash,do2_hash,do3_hash,do4_hash).transact() #Blockchain Function code 
        print('Request has been accepted. Transaction successsfull')
    elif status == '0':
        ack = db_meths.request_handler(status,land_id,from_user_id)
        if ack==1:
            print('Request has been declined')
        else:
            print('Request has not been declined. Please try again later')
    return redirect('/profile')


if __name__ == "__main__": 
    app.run(debug = True, threaded=True) 


