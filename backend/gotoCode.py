from connectSAP import connect_to_sap
import time
from flask import jsonify

def gotoCO11N():
    try:
        

        session = connect_to_sap()
        session.findById("wnd[0]").maximize()
        session.findById("wnd[0]/tbar[0]/okcd").text = "/nCO11N"
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(0.5)
    except Exception as e:
        print(e)
        return jsonify({'Error': str(e)})