from flask import *
from models import app

from Home_route import home_auth_bp
app.register_blueprint(home_auth_bp)

from Create_Alert_route import create_alert_auth_bp
app.register_blueprint(create_alert_auth_bp)

from Update_Stock_Data_route import update_stock_data_auth_bp
app.register_blueprint(update_stock_data_auth_bp)

from Save_alert_db_route import save_alert_db_auth_bp
app.register_blueprint(save_alert_db_auth_bp)

from Download_Stock_Data_route import download_stock_data_auth_bp
app.register_blueprint(download_stock_data_auth_bp)

from Check_Triggered_Alert_route import check_triggered_alert_auth_bp
app.register_blueprint(check_triggered_alert_auth_bp)

from Customised_Index_route import customised_index_auth_bp
app.register_blueprint(customised_index_auth_bp)

#Checks if the run.py file has executed directly and not imported
if __name__ == "__main__" :
    app.run(debug=True, port=8000)