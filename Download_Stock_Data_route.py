from flask import *
import sqlite3
from nsetools import Nse
from tqdm import tqdm
import yfinance as yf
import pandas as pd

download_stock_data_auth_bp = Blueprint('download_stock_data_auth', __name__)

@download_stock_data_auth_bp.route("/Download_Stock_Data",methods=['GET','POST'])

def download_data() :

    connection_tabledb = sqlite3.connect('C:/Users/Pranay/Desktop/Work_Folder/Folders/Flask_ALERT/instance/table.db')
    cursor_tabledb = connection_tabledb.cursor()

    connection_stockdb = sqlite3.connect('C:/Users/Pranay/Desktop/Work_Folder/Folders/Flask_ALERT/instance/stock.db')
    cursor_stockdb = connection_stockdb.cursor()   

    import datetime
    current_time = datetime.datetime.now().time()
    start_time = datetime.time(1, 45)
    end_time = datetime.time(23, 55)

    if start_time <= current_time <= end_time:

        df = pd.read_csv('./nse_cm.csv')
        df_filt = df[df['pGroup'] == 'EQ'].copy()
        nse_stock_list = df_filt.pSymbolName.unique()
    
        for i in tqdm(nse_stock_list) :
            symbol = i
            for j in ['-','&'] :
                if j in symbol :
                    symbol = symbol.replace(j,'_')
            
            table_name = "nse_" + symbol

            cursor_stockdb.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (Date date,Open int, High int, Low int, Close int, Volume int)")
            cursor_stockdb.execute(f"SELECT Date FROM {table_name} WHERE Date =(SELECT max(Date) FROM {table_name})")

            query_output = cursor_stockdb.fetchall()
                       
            if query_output :
                from datetime import datetime
                result = datetime.strptime( query_output[0][0], "%Y-%m-%d" ).date()
                data = yf.download(i+".NS", start=result)
            else :
                data = yf.download(i+".NS", period = 'max')
            
            data = data.round(decimals = 2)
            data.reset_index( inplace = True )
            data.drop('Close',axis = 1, inplace = True)
            data.rename(columns = {'Adj Close' : 'Close'},inplace = True)
            import datetime
            data.Date = [d.date() for d in data.Date]

            if data.empty :
                cursor_stockdb.execute(f"DROP TABLE {table_name}")
            else :  
                if query_output :
                    data.iloc[1:].to_sql(table_name, connection_stockdb, if_exists='append', index = False)
                else :
                    data.to_sql(table_name, connection_stockdb, if_exists='append', index = False)

        table_names = cursor_stockdb.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
        for i in table_names :
            stock_symbol = i[0]
            last_row = cursor_stockdb.execute(f"SELECT Close FROM '{stock_symbol}' ORDER BY Date DESC LIMIT 1").fetchone()
            cursor_tabledb.execute(f"UPDATE alert_create SET Current_price = {last_row[0]} WHERE Stock_symbol = '{stock_symbol}';")
            connection_tabledb.commit()
    
    return redirect('/Update_Stock_Data')
