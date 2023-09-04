from flask import Blueprint
import sqlite3
import pandas as pd
from flask import render_template

home_auth_bp = Blueprint('home_auth', __name__)

@home_auth_bp.route("/Home",methods=['GET','POST'])
@home_auth_bp.route("/",methods=['GET','POST'])

def start_page() :

    connection_tabledb = sqlite3.connect('C:/Users/Pranay/Desktop/Work_Folder/Folders/Flask_ALERT/instance/table.db')
    cursor_tabledb = connection_tabledb.cursor()

    connection_stockdb = sqlite3.connect('C:/Users/Pranay/Desktop/Work_Folder/Folders/Flask_ALERT/instance/stock.db')
    cursor_stockdb = connection_stockdb.cursor()

    df = pd.read_csv('C:/Users/Pranay/Desktop/Work_Folder/Folders/Flask_Alert/stock_sector_industry.csv')
    df_nse = df[df['Exchange'] == "NSE"].copy()
    df_nse.reset_index(drop = True, inplace = True)

    table_names = cursor_stockdb.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    for i in table_names :
        stock_symbol = i[0]

        result = cursor_tabledb.execute(f"SELECT Stock_symbol from alert_create where Stock_symbol = '{stock_symbol}' ").fetchone()
        
        if result :
            pass
        else :
            try :
                df_index = df_nse[df_nse['Symbol'] == stock_symbol.split('_',1)[1]].index[0]
            except IndexError :
                df_sector = 'NA'
                df_industry = 'NA'
                df_mcap = 'NA'
            else :
                df_sector = df_nse['Sector'].iloc[df_index]
                df_industry = df_nse['Industry'].iloc[df_index]
                df_mcap = df_nse['Market Cap(Rs. Cr.)'].iloc[df_index]

            finally :
                cursor_tabledb.execute(f"INSERT INTO alert_create (Stock_symbol, Sector, Industry, Mcap) VALUES ('{stock_symbol}', '{df_sector}', '{df_industry}', '{df_mcap}');")
                connection_tabledb.commit()  

    unique_sectors = cursor_tabledb.execute("SELECT Distinct Sector from alert_create").fetchall()
    unique_sectors = [sector[0] for sector in unique_sectors]

    unique_industry = cursor_tabledb.execute("SELECT Distinct Industry from alert_create").fetchall()
    unique_industry = [industry[0] for industry in unique_industry]

    return render_template('Home.html', sectors_list = unique_sectors, industry_list = unique_industry )
