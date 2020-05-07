from LRDB import db

class fm_profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    username = db.Column(db.String(80))
    fname = db.Column(db.String(80))
    lname = db.Column(db.String(80))
    email = db.Column(db.String(120))
    pswd = db.Column(db.String(80))
    addr = db.Column(db.String(200))
    city = db.Column(db.String(80))
    country = db.Column(db.String(80))
    admin = db.Column(db.Integer)

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

class land_requests(db.Model):
    req_id = db.Column(db.Integer, primary_key=True)
    Land_ID = db.Column(db.Integer)
    To_user = db.Column(db.String(80))
    From_user = db.Column(db.String(80))
    status = db.Column(db.Integer)
    to_user_id = db.Column(db.Integer)
    from_user_id = db.Column(db.Integer)

class transactions(db.Model):
    t_id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(100))
    use_case = db.Column(db.String(80))
