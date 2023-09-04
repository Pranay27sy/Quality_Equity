from flask_sqlalchemy import SQLAlchemy
from flask import *

app = Flask(__name__)
app.secret_key = 'alert_app_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///table.db'
app.config['SQLALCHEMY_BINDS'] = {'db1' : 'sqlite:///stock.db'}

db = SQLAlchemy(app)

class ALERT(db.Model):
    __bind_key__ = None
    __tablename__ = 'alert_create'

    id = db.Column(db.Integer, primary_key=True)
    Stock_symbol = db.Column( db.String(255), unique=True)
    Sector = db.Column( db.String(255))
    Industry = db.Column( db.String(255))
    Mcap = db.Column( db.Integer )
    Current_price = db.Column( db.Integer )
    Breakdown_price = db.Column( db.Integer )
    Breakout_price = db.Column( db.Integer )
    Last_updated = db.Column(db.Date)

    def __repr__(self) :
        return f'{self.Stock_symbol}'
    

with app.app_context():
    db.create_all()