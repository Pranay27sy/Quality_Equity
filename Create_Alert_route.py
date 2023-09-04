from flask import *
import sqlite3
import pandas as pd

create_alert_auth_bp = Blueprint('create_alert_auth', __name__)

@create_alert_auth_bp.route("/Create_Alert",methods=['GET','POST'])
def alert_page():
    if request.method == 'POST' :
        session['sector_select'] = request.form['sector_dropdown']

    connection_tabledb = sqlite3.connect('C:/Users/Pranay/Desktop/Work_Folder/Folders/Flask_ALERT/instance/table.db')

    alert_create_df = pd.read_sql_query(f"SELECT * FROM alert_create", connection_tabledb)
    alert_create_filt = alert_create_df[alert_create_df['Sector'] == session['sector_select'] ].copy()
    alert_create_filt.reset_index(drop = True, inplace = True)
    
    data_set_1 = pd.read_csv("C:/Users/Pranay/Desktop/Work_Folder/Folders/Flask_Alert/NSE_stocks_official_indices.csv")
    imp_stocks_list = data_set_1['Stock_Symbol'].to_list()
    pass_stock_list = []
    for i in list(alert_create_filt['Stock_symbol'].unique()) :
        if i.split("_",1)[1] in imp_stocks_list :
            pass_stock_list.append(i)
    return render_template('create_alert.html',items= alert_create_filt )

