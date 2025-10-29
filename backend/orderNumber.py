import time
from flask import jsonify
from connectSAP import connect_to_sap

session = connect_to_sap()

def OrderNumber(order_number):
    for _ in range(3):
            try:
                time.sleep(2)
                jsonify({'status':"[INFO] Attempting to handle confirmation dialog..."})
                session.findById("wnd[1]/usr/btnSPOP-OPTION2").press()
                time.sleep(0.5)
                session.findById("wnd[1]/usr/btnBUTTON_1").press()
                time.sleep(0.5)
                session.findById("wnd[1]/tbar[0]/btn[0]").press()
            except:
                pass
                status_bar_text = session.findById("wnd[0]/sbar").Text
            
                
            words = status_bar_text.split()
        
            # Look for the first word that looks like a document number (all digits)
            for word in words:
                if word.isdigit() and len(word) >= 10:
                    vf = word

            return f"Order {order_number} processed successfully Document Number generated {vf}"