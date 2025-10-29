from flask import Flask, request, jsonify
from flask_cors import CORS
import win32com.client
import time
import pythoncom
import pandas as pd

app = Flask(__name__)
CORS(app)
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
RESET = '\033[0m'


session = None



def connect_to_sap():
    global session
    pythoncom.CoInitialize()  # Initialize COM library for this thread
    try:
        SapGuiAuto = win32com.client.GetObject("SAPGUI")
        application = SapGuiAuto.GetScriptingEngine
        connection = application.Children(0)
        session = connection.Children(0)
        print("[INFO] Connected to SAP session.")
        
        return session
    except Exception as e:
        raise ConnectionError(f"Could not connect to SAP GUI: {str(e)}")


def process_order(order_number, shift, quantity, operation_type, operation=None):
    connect_to_sap()

    session.findById("wnd[0]").maximize()
    session.findById("wnd[0]/tbar[0]/okcd").text = "/nCO11N"
    session.findById("wnd[0]").sendVKey(0)
    time.sleep(0.5)

    session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_HDR:SAPLCORU_S:0110/ctxtAFRUD-AUFNR").text = order_number
    session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_HDR:SAPLCORU_S:0110/ctxtAFRUD-VORNR").setFocus()
    session.findById("wnd[0]").sendVKey (4)

    
    time.sleep(0.5)
    
    count = 0
    
    for i in range(50):
        try:
            shell = session.findById(f"wnd[1]/usr/sub/1[0]/sub/1/2[0]/sub/1/2/15[0,15]/lbl[1,{i}]")
            count += 1
            process = ''
            process = shell.Text
            
        except Exception:
            # Element with this index does not exist
            continue
    session.findById("wnd[1]/tbar[0]/btn[12]").press()

        
    
    row_count = count + 1
    print(row_count)
    last_row = row_count
    first_row = 0
    print(f"[INFO] Last row: {last_row}, First row: {first_row}")

    if operation_type == 'A':
        if row_count == 0:
            raise ValueError("No operations found in the order.")
        last_row = count - 1
        try:
            session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_HDR:SAPLCORU_S:0110/ctxtAFRUD-VORNR").caretPosition = 0
            session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_HDR:SAPLCORU_S:0110/ctxtAFRUD-VORNR").text = process
            session.findById('wnd[0]').sendVKey(0)
        except:
            print()
        is_last = True
        raise ValueError("Invalid operation type")
    qty_field = session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_DET1:SAPLCORU_S:0200/txtAFRUD-LMNGA")
    qty_field.text = quantity
    qty_field.setFocus()
    session.findById("wnd[0]/tbar[1]/btn[18]").press()
    session.findById("wnd[0]").sendVKey(0)
    try:
        session.findById("wnd[1]").sendVKey(0)  
    except:
        pass
    time.sleep(0.5)

    shift_combo = session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_DET2:SAPLCORU_S:0910/subSLCUST:SAPLXCOF:0910/cmbAFRUD-SHIFT")
    print(f"[INFO] Setting shift to {shift}")
    shift_combo.key = shift
    
    session.findById("wnd[0]").sendVKey(0)
    print(f"success")
    session.findById("wnd[0]/tbar[1]/btn[18]").press()
    
    
    time.sleep(0.5)

    if operation_type == 'A':
        time.sleep(0.5)
        session.findById("wnd[0]/usr/subPUSHBUTTON:SAPLCOWB:0400/btnMALL").press()
        
        time.sleep(0.5)
        session.findById("wnd[0]/usr/subTABLE:SAPLCOWB:0500/tblSAPLCOWBTCTRL_0500").getAbsoluteRow(0).selected = False
        session.findById("wnd[0]/usr/subTABLE:SAPLCOWB:0500/tblSAPLCOWBTCTRL_0500/ctxtCOWB_COMP-MATNR[0,0]").setFocus()
        session.findById("wnd[0]/usr/subPUSHBUTTON:SAPLCOWB:0400/btnCHFI").press()
        
        time.sleep(3)
        time.sleep(0.5)
    elif operation_type == 'B':
        time.sleep(0.5)
        session.findById("wnd[0]/usr/subPUSHBUTTON:SAPLCOWB:0400/btnMALL").press()
        session.findById("wnd[0]/usr/subPUSHBUTTON:SAPLCOWB:0400/btnCHFI").press()

        time.sleep(0.5)
    elif operation_type == 'B' and is_last:
        time.sleep(0.5)
        session.findById("wnd[0]/usr/subPUSHBUTTON:SAPLCOWB:0400/btnMALL").press()
        time.sleep(0.5)
        session.findById("wnd[0]/usr/subTABLE:SAPLCOWB:0500/tblSAPLCOWBTCTRL_0500").getAbsoluteRow(0).selected = False
        session.findById("wnd[0]/usr/subTABLE:SAPLCOWB:0500/tblSAPLCOWBTCTRL_0500/ctxtCOWB_COMP-MATNR[0,0]").setFocus()
        session.findById("wnd[0]/usr/subPUSHBUTTON:SAPLCOWB:0400/btnCHFI").press()
        
        time.sleep(0.5)

    
    session.findById("wnd[0]/tbar[0]/btn[11]").press()
    
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


@app.route("/process", methods=["POST"])
def process():
    try:
        data = request.json
        order_number = data.get("order_number")
        shift = data.get("shift")
        quantity = data.get("quantity")
        operation_type = data.get("operation_type")
        operation = data.get("operation")

        if not all([order_number, shift, quantity, operation_type]):
            return jsonify({"error": "Missing required fields"}), 400

        message = process_order(order_number, shift, quantity, operation_type, operation)
        return jsonify({
            "status": "success",
            "order_number": order_number,
            "operation": operation,
            "message": message
        }), 200

    except Exception as e:
        e = 'Invalid Order Number'
        return jsonify({"Error ": str(e)}), 500


@app.route("/getOperations", methods=["POST"])
def get_operations():
    try:
        data = request.json
        order_number = data.get("order_number")
        connect_to_sap()
        session.findById("wnd[0]").maximize()
        session.findById("wnd[0]/tbar[0]/okcd").text = "/nCO11N"
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(0.5)

        # Input order number
        session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_HDR:SAPLCORU_S:0110/ctxtAFRUD-AUFNR").text = order_number
        session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_HDR:SAPLCORU_S:0110/ctxtAFRUD-VORNR").setFocus()
        session.findById("wnd[0]").sendVKey(4)
        time.sleep(0.5)
        ops = []
        count = 0
        for i in range(3,50): 
            try:
                shell = session.findById(f"wnd[1]/usr/sub/1[0]/sub/1/2[0]/sub/1/2/15[0,15]/lbl[1,{i}]")
                shell.setFocus()
                ops.append(shell.Text)
                print(ops)
                count += 1
            except Exception as e:
                return jsonify({'Operation not found'})
            break
        return jsonify({"operations": ops}), 200
    
    except Exception as e:
        print("[ERROR] getOperations:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/btchdtr", methods=["POST"])
def btchDtr():
    try:
        mvmt = '311'
        plant = '1002'
        file =  request.files.get("file")
        
        if not file:
            return jsonify({'error':'File is required'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Only CSV files are supported',
                            "status": "success",
                            "plant": plant}), 400
        
        df = pd.read_csv(file)
        materials = df['Material'].astype(str).tolist()
        qty = df['Quantity'].astype(str).tolist() 
        unit = df['UnE'].astype(str).tolist()
        recloc = df['Receiving Location'].astype(str).tolist()
        strloc = df['Storage Location'].astype(str).tolist()

        print(f"[INFO] Processing {len(materials)} materials for plant {plant[0]}")
        filtered_df = df[df['Material'].isin(materials)]

        
        connect_to_sap()  # Ensure session is global or passed
        session.findById("wnd[0]").maximize()
        session.findById("wnd[0]/tbar[0]/okcd").text = "/nMB21"
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(0.5)

        mvmtfield = session.findById("wnd[0]/usr/ctxtRM07M-BWART")
        if mvmtfield:
            mvmtfield.text = mvmt

        plantfield = session.findById("wnd[0]/usr/ctxtRM07M-WERKS")
        if plantfield:
            plantfield.text = plant

        time.sleep(0.8)
        session.findById("wnd[0]").sendVKey(0)

        session.findById("wnd[0]/usr/ctxtRKPF-UMLGO").text = recloc[0]
        total_materials = len(materials)
        batch_size = 14
        idx = 0
        while idx < total_materials:
            end_idx = min(idx + batch_size, total_materials)
            for row in range(idx, end_idx):
                row_offset = row - idx  # SAP row index for this batch (0 to 13)
                # Iterate through rows, not columns. row_offset is the SAP row index, 7 is the column for Material.
                session.findById(f"wnd[0]/usr/sub:SAPMM07R:0521/ctxtRESB-MATNR[{row_offset},7]").text = materials[row]
                session.findById(f"wnd[0]/usr/sub:SAPMM07R:0521/txtRESB-ERFMG[{row_offset},48]").text = qty[row]
                session.findById(f"wnd[0]/usr/sub:SAPMM07R:0521/ctxtRESB-ERFME[{row_offset},66]").text = unit[row]
                session.findById(f"wnd[0]/usr/sub:SAPMM07R:0521/ctxtRESB-LGORT[{row_offset},76]").text = strloc[row]
                session.findById('wnd[0]').sendVKey(0)
                session.findById('wnd[0]').sendVKey(0)
            
            session.findById("wnd[0]/tbar[1]/btn[7]").press()
            idx += batch_size


        
        session.findById("wnd[0]/tbar[0]/btn[11]").press()
        time.sleep(2)
        status_bar_text = session.findById("wnd[0]/sbar").Text
        
            
        words = status_bar_text.split()
        
        # Look for the first word that looks like a document number (all digits)
        for word in words:
            if word.isdigit() and len(word) >= 10:
                vf = word
        message = f"Material reservation created  Document : {vf}"

        return jsonify({
            "status": "success",
            "mvmt": mvmt,
            "plant": plant,
            "message": message
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500




@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, port=5001) 
 
