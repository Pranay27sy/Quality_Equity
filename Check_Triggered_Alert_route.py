from flask import *
import sqlite3
from datetime import datetime
import pandas as pd

check_triggered_alert_auth_bp = Blueprint('check_triggered_alert_auth', __name__)
 


@check_triggered_alert_auth_bp.route("/Check_Triggered_Alert",methods=['GET','POST']) 

def ALERT_triggered():

    connection_tabledb = sqlite3.connect('C:/Users/Pranay/Desktop/Work_Folder/Folders/Flask_ALERT/instance/table.db')
    cursor_tabledb = connection_tabledb.cursor()

    connection_stockdb = sqlite3.connect('C:/Users/Pranay/Desktop/Work_Folder/Folders/Flask_ALERT/instance/stock.db')
    cursor_stockdb = connection_stockdb.cursor()

    df_alert_template = pd.DataFrame(columns = ['Symbol','Sector','alert_create_date','alert_trigger_date','Alert_Type'])

    alert_create_df = pd.read_sql_query("SELECT * FROM alert_create", connection_tabledb)
    alert_create_filt = alert_create_df[alert_create_df['Last_updated'].notnull()].reset_index(drop = True)

    for index, row in alert_create_filt.iterrows():
        stock_name = row['Stock_symbol']
        stock_sector = row['Sector']
        breakdown_price = row['Breakdown_price']
        breakout_price = row['Breakout_price']
        alert_create_date = datetime.strptime( row['Last_updated'] , "%Y-%m-%d" ).date()

        if stock_name not in pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", connection_stockdb)['name'].values :
            pass
        else :
            stock_OHLC = pd.read_sql_query(f"SELECT * FROM {stock_name}", connection_stockdb)
            # convert the date strings to datetime objects
            stock_OHLC['Date'] = pd.to_datetime(stock_OHLC['Date'], format='%Y-%m-%d')

            # extract the date component from the datetime column
            stock_OHLC['Date'] = stock_OHLC['Date'].dt.date

            stock_OHLC_filt = stock_OHLC[stock_OHLC['Date'] > alert_create_date ].reset_index(drop = True)
            for idx, row_ohlc in stock_OHLC_filt.iterrows():
                close_price = row_ohlc['Close']
                alert_trigger_date = row_ohlc['Date']
                if breakdown_price is not None :
                    if close_price < breakdown_price:
                        row_dict = {'Symbol' : stock_name, 'Sector' : stock_sector,'alert_create_date' : alert_create_date
                                    ,'alert_trigger_date' : alert_trigger_date, 'Alert_Type' : "Breakdown"}
                        row_df = pd.DataFrame(row_dict, index=[0])  
                        df_alert_template = pd.concat([df_alert_template,row_df])  
                        break

                if breakout_price is not None :
                    if close_price > breakout_price :
                        row_dict = {'Symbol' : stock_name, 'Sector' : stock_sector,'alert_create_date' : alert_create_date
                                    ,'alert_trigger_date' : alert_trigger_date, 'Alert_Type' : "Breakout"}
                        row_df = pd.DataFrame(row_dict, index=[0])  
                        df_alert_template = pd.concat([df_alert_template,row_df])  
                        break

    df_alert_template = df_alert_template.sort_values( by = 'alert_trigger_date', ascending = False )
    df_alert_template.reset_index(drop = True, inplace = True)

    return render_template('alert_trigger.html', items = df_alert_template )
