from flask import *
import sqlite3
import pandas as pd
from tqdm import tqdm
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

customised_index_auth_bp = Blueprint('customised_index_auth', __name__)

@customised_index_auth_bp.route("/Customised_index",methods=['GET','POST'])

def customised_index() :

    connection_tabledb = sqlite3.connect('C:/Users/Pranay/Desktop/Work_Folder/Folders/Flask_ALERT/instance/table.db')
    alert_create_df = pd.read_sql_query("SELECT * FROM alert_create", connection_tabledb)

    if request.method == 'POST' :
        for key, value in request.form.items():
            if key == 'sector_dropdown' :
                sector_or_industry_df = alert_create_df[alert_create_df['Sector'] == value ].copy()
                sector_or_industry_df.reset_index(drop = True, inplace = True)
            elif key == 'industry_dropdown' :
                sector_or_industry_df = alert_create_df[alert_create_df['Industry'] == value ].copy()
                sector_or_industry_df.reset_index(drop = True, inplace = True)
        

    connection_stockdb = sqlite3.connect('C:/Users/Pranay/Desktop/Work_Folder/Folders/Flask_ALERT/instance/stock.db')

    trading_days = 250
    No_of_stocks = 0 
    index_value_list = []
    stocks_in_cust_indice = []
    sbin_df = pd.read_sql_query("SELECT * FROM nse_SBIN", connection_stockdb)
    sbin_filt = sbin_df.tail(trading_days)
    sbin_filt.reset_index(drop = True, inplace = True)
    sbin_filt['Date'] = pd.to_datetime(sbin_filt['Date'], format='%Y-%m-%d')
    sbin_filt['Date'] = sbin_filt['Date'].dt.date

    for i in tqdm(sector_or_industry_df['Stock_symbol'].unique()) :
        one_list = []
        
        try :
            stock_df = pd.read_sql_query(f"SELECT * FROM {i}", connection_stockdb)
        except pd.errors.DatabaseError: 
            pass
        else :
            df2 = stock_df[['Date','Close']].copy()
            if len(df2) >= trading_days :
                df3 = df2.tail(trading_days)
                df3.reset_index( drop = True, inplace = True )
                df3['Date'] = pd.to_datetime(df3['Date'], format='%Y-%m-%d')
                df3['Date'] = df3['Date'].dt.date

                if sbin_filt['Date'].equals(df3['Date']) :
                    stocks_in_cust_indice.append(i.split('_',1)[1])
                    No_of_stocks +=1
                    
                    if No_of_stocks == 1 :
                        index_value_list = [0]*(len(df3)-1)
                    for j in range(1,len(df3)) :
                        diff = ((df3['Close'][j] - df3['Close'][j-1])/df3['Close'][j-1] )*100
                        one_list.append(diff)
                    index_value_list = [x+y for x,y in zip(index_value_list, one_list)]
            
    index_value_list = [x/No_of_stocks for x in index_value_list]  

    final_list = [100]
    pointer = 100
    for i in index_value_list :
        pointer = pointer + i
        final_list.append(pointer)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sbin_filt["Date"], y=final_list ) )
    fig.update_traces(mode='lines')
    fig.update_layout(title= value , xaxis_title="Date", yaxis_title="Price" )

    # Render the template with the plot
    return render_template('customised_index_plot.html', plot=fig.to_html(full_html=False) ,stock_list = stocks_in_cust_indice )
