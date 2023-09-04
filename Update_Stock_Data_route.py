from flask import *
import sqlite3
import sqlalchemy

update_stock_data_auth_bp = Blueprint('update_stock_data_auth', __name__)

@update_stock_data_auth_bp.route("/Update_Stock_Data",methods=['GET','POST'])
def yahoo_f() :

    connection_stockdb = sqlite3.connect('C:/Users/Pranay/Desktop/Work_Folder/Folders/Flask_ALERT/instance/stock.db')
    cursor_stockdb = connection_stockdb.cursor()

    try :
        last_row = cursor_stockdb.execute("SELECT Date FROM nse_SBIN ORDER BY Date DESC LIMIT 1").fetchone()
        last_date = last_row[0]
    except sqlalchemy.exc.OperationalError :
        last_date = "Empty Database"
    from datetime import date
    today = date.today()

    return render_template('update_stock_data.html',last_date = last_date, today_date = today)