from flask import *
import sqlite3
from datetime import datetime
from models import db, ALERT


save_alert_db_auth_bp = Blueprint('save_alert_db_auth', __name__)

@save_alert_db_auth_bp.route("/Save_alert_db",methods=['GET','POST'])

def submit_data() :
    connection_tabledb = sqlite3.connect('C:/Users/Pranay/Desktop/Work_Folder/Folders/Flask_ALERT/instance/table.db')
    cursor_tabledb = connection_tabledb.cursor()

    connection_stockdb = sqlite3.connect('C:/Users/Pranay/Desktop/Work_Folder/Folders/Flask_ALERT/instance/stock.db')
    cursor_stockdb = connection_stockdb.cursor()

    if request.method == 'POST' :

        for key, value in request.form.items():
            if key.startswith("breakdown_"):
                input_id = key.split("_")[1]
                # Check which button was clicked
                if request.form.get(f"button_{input_id}") :
                    stocking = ALERT.query.get(input_id)
                    try :
                        breakdown = float(request.form[f"breakdown_{input_id}"])

                    except ValueError :
                        pass

                    else :
                        if breakdown < stocking.Current_price :
                            stocking.Breakdown_price = breakdown
                            stocking.Last_updated = datetime.today().date()
                            db.session.commit()

                    try :
                        breakout  = float(request.form[f"breakout_{input_id}"])

                    except ValueError :
                        pass

                    else :
                        if breakout > stocking.Current_price :
                            stocking.Breakout_price  = breakout
                            stocking.Last_updated = datetime.today().date()        
                            db.session.commit()

                if request.form.get(f"clear_{input_id}") :
                    stocking = ALERT.query.get(input_id)
                    stocking.Breakdown_price = None
                    stocking.Breakout_price  = None
                    stocking.Last_updated = None
                    db.session.commit()

                return redirect('/Create_Alert')