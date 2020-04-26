from flask import render_template,Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/lrdb'
db = SQLAlchemy(app)


class fm_profiles(db.Model):
    
    fname = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    email = db.Column(db.String(120))
    pswd = db.Column(db.String(80))
    id = db.Column(db.Integer, primary_key=True)

class land_details(db.Model):

    id = db.Column(db.Integer)
    fname = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    doc1 = db.Column(db.LargeBinary())
    doc2 = db.Column(db.LargeBinary())
    doc3 = db.Column(db.LargeBinary())
    doc4 = db.Column(db.LargeBinary())
    land_id = db.Column(db.Integer, primary_key=True)
    sell = db.Column(db.Integer)
    size = db.Column(db.Integer)
    price = db.Column(db.Integer)
    loc = db.Column(db.String(80))

# class requests(db.Model):
    
#     Land_id = db.Column(db.Integer)
#     To_user = db.Column(db.String(80))
#     From_user = db.Column(db.String(80))
#     status = db.Column(db.Integer)
#     to_user_id = db.Column(db.Integer)
#     from_user_id = db.Column(db.Integer)


#Database Store
def set_prof123(fname, lname, email, pswd, uid):
    try:
        register = fm_profiles(fname=fname,lname=lname,email=email,pswd=pswd,id=uid)
        db.session.add(register)
        db.session.commit()
    except:
        print("Error")
        return 0

@app.route('/')
def index():
    set_prof123('Uvais','Chudesra','uvais1907@gmail.com','asd','120')
    return render_template('home.html')

if __name__ == "__main__": 
    app.run(debug = True, threaded=True) 


# def get_prof(email, password):
#     try:
#         sql_fetch_blob_query = """SELECT * from fm_profiles where email = %s"""
#         cursor.execute(sql_fetch_blob_query, (email,))
#         record = cursor.fetchone()
#         if record[3] == password:
#             return record
#         else:
#             print('fail')
#             return 0
#     finally:
#         if (connection.ping()):
#             cursor.close()

# def get_prof_id(id):
#     try:
#         sql_fetch_blob_query = """SELECT * from fm_profiles where id = %s"""
#         cursor.execute(sql_fetch_blob_query, (id,))
#         record = cursor.fetchone()
#         if record != None:
#             return record
#         else:
#             print('fail')
#             return 0
#     finally:
#         if (connection.ping()):
#             cursor.close()

        
# def set_land(id, fname, lname, doc1, doc2, doc3, doc4, loc, size):
#     land_id = random.randint(1,1000)
#     sell = 0
#     price = 0
#     print("Inserting Documents into Land_Details Table")
#     try:
#         sql_insert_query = """ INSERT INTO land_details
#                           (id, fname, lname, doc1, doc2, doc3, doc4, land_id, sell, size, price, loc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

#         # Convert data into tuple format
#         insert_tuple = (id, fname, lname, doc1, doc2, doc3, doc4, land_id, sell, size, price, loc)
#         result = cursor.execute(sql_insert_query, insert_tuple)
#         connection.commit()
#         print("Documents inserted successfully into Test_Block Table", result)
#         return 1
#     except (pymysql.Error) as e:
#         print('Error',e)
#         return 0
#     finally:
#         if (connection.ping()):
#             cursor.close()
#             print("MySQL connection is closed")

# def get_land(uid):

#     try:
#         sql_fetch_blob_query = """SELECT * from land_details where id = %s"""
#         cursor.execute(sql_fetch_blob_query, (uid,))
#         record = cursor.fetchall()
#         return record
#     finally:
#         if(connection.ping()):
#             cursor.close()

# def get_land_uid(uid,land_id):

#     try:
#         sql_fetch_blob_query = """SELECT * from land_details where id =%s and land_id = %s"""
#         cursor.execute(sql_fetch_blob_query, (uid, land_id,))
#         record = cursor.fetchone()
#         return record
#     except (pymysql.Error) as e:
#         print('Error',e)
#     finally:
#         if(connection.ping()):
#             cursor.close()

# def get_land_sell():

#     try:
#         sql_fetch_blob_query = """SELECT * from land_details where sell = 1"""
#         cursor.execute(sql_fetch_blob_query)
#         record = cursor.fetchall()
#         return record
#     finally:
#         if(connection.ping()):
#             cursor.close()


# def set_requests(land_id,To_user,From_user,to_user_id,from_user_id):
#     try:
#         sql_insert_query = """ INSERT INTO requests (Land_ID, To_user, From_user,to_user_id, from_user_id) VALUES (%s,%s,%s,%s,%s)"""
#         insert_tuple=(land_id,To_user,From_user,to_user_id,from_user_id)
#         cursor.execute(sql_insert_query,insert_tuple)
#         record = cursor.fetchall()
#         connection.commit()
#         return 1
#     except (pymysql.Error) as e:
#         return 0
#     finally:
#         if(connection.ping()):
#             cursor.close()
    
# def get_requests(To_user):
#     try:
#         sql_fetch_blob_query = """SELECT * from requests where To_user=%s"""
#         cursor.execute(sql_fetch_blob_query,(To_user,))
#         record = cursor.fetchall()
#         return record
#     finally:
#         if(connection.ping()):
#             cursor.close()


# def request_handler(status,land_id,from_user_id):

#     try:
#         sql_update_query = "update land_details set id = %s, fname=%s, lname=%s, sell=NULL, price=0 where land_id = %s"
#         sql_delete_query =  "delete from requests where Land_id = %s and from_user_id = %s"
#         prof1 = get_prof_id(from_user_id)
#         if status=='1':
#             cursor.execute(sql_update_query,(from_user_id,prof1[0],prof1[1],int(land_id),))
#             cursor.execute(sql_delete_query,(land_id,from_user_id,))
#             connection.commit()
#             print('Accept Done')
#         else:
#             cursor.execute(sql_delete_query,(land_id,from_user_id,))
#             connection.commit()
#             print('Decline done')
#         return 1
#     except (pymysql.Error) as e:
#         print(e)
#         return 0
#     finally:
#         if(connection.ping()):
#             cursor.close()
    
# def sell_land(land_id,price):
#     try:
#         sql_query = """UPDATE land_details SET sell = 1, price= %s where land_id = %s"""
#         data = (price,land_id)
#         cursor.execute(sql_query,data)
#         connection.commit()
#         return 1
#     except (pymysql.Error) as e:
#         print(e)
#         return 0
#     finally:
#         if(connection.ping()):
#             cursor.close()
#             connection.close()
