from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key='hello mellow jello'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/lrdb'
app.url_map.strict_slashes = False
db = SQLAlchemy(app)

from LRDB import models
from LRDB import routes
from LRDB import bc_settings