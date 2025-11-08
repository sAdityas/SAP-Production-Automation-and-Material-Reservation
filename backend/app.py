from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import pandas as pd
import sys
from connectSAP import connect_to_sap
from ProcessOrder import process_order
from gotoCode import gotoCO11N
from enterOrderNumber import enterNumber

app = Flask(__name__)
CORS(app)
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
RESET = '\033[0m'


session = connect_to_sap()

@app.route("/process", methods=["POST"])
def process():
    try:
        data = request.json
        order_number = data.get("order_number")
        shift = data.get("shift")
        quantity = data.get("quantity")
        operation_type = data.get("operation_type")
        operation = data.get("operation")
        print(data)
        if not all([order_number, shift, quantity, operation_type]):
            return jsonify({"error": "Missing required fields"}), 400

        message = process_order(order_number, shift, quantity, operation_type, operation)
        return jsonify({
            "message": message,
            "operation_type" : operation_type,
            "shift" : shift,
            "quantity" : quantity,
            "msg" : "Order Processed Successfully"
        }) , 200

    except Exception as e:
        print(e)
        return jsonify({"Error ": "Invalid Order Number"})


@app.route("/getOperations", methods=["POST"])
def get_operations():
    try:
        data = request.json
        order_number = data.get("order_number")
        session =connect_to_sap()

        gotoCO11N()

        # Input order number
        enterNumber(order_number)
        time.sleep(0.5)
        ops = []

        shell = session.findById("wnd[1]/usr/cntlCUSTOM_CONTAINER/shellcont/shell")
        row_count = shell.RowCount
        print(f"Total rows found: {row_count}")
        for i in range(row_count):
            try:
                time.sleep(0.2)
                # Read value from specific column (e.g., "VORNR" or "ARBPL" etc.)
                process_text = shell.GetCellValue(i, "F0001")  # <-- Change column name
                ops.append(process_text)
                print(f"Row {i}: {process_text}")

            except Exception as e:
                print(f"Error on row {i}: {e}")
                continue

        # Close the popup
        session.findById("wnd[1]/tbar[0]/btn[12]").press()

        # for i in range(3,50): 
        #     try:
        #         shell = session.findById(f"wnd[1]/usr/sub/1[0]/sub/1/2[0]/sub/1/2/15[0,15]/lbl[1,{i}]")
        #         shell.setFocus()
        #         ops.append(shell.Text)
        #         print(ops)
        #         count += 1
        #     except Exception as e:
        #         break  # Stop if no more operations are found
        # if not ops:
        #     raise Exception("No operations available")
        # return jsonify({"operations": ops}), 200

        if not ops:
            raise Exception("No operations available")
        return jsonify({"operations": ops}), 200

    except Exception as e:
        return jsonify({"error": "Error while getting Operations check SAP."}), 500

@app.route("/btchdtr", methods=["POST"])
def btchDtr():
    try:
        

        
        session = connect_to_sap()  # Ensure session is global or passed
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


        print(f"[INFO] Processing {len(materials)} materials for plant {plant}")
        filtered_df = df[df['Material'].isin(materials)]
        print("123154",filtered_df.head())
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
        nanmats = 0
        if 'nan' or "" in materials:
            nanmats += 1
        total_materials -= nanmats
        print(total_materials)
        batch_size = 14
        idx = 0
        while idx < total_materials:
            end_idx = min(idx + batch_size, total_materials)
            for row in range(idx, end_idx):
                row_offset = row - idx  
                # SAP row index for this batch (0 to 13)
                # Iterate through rows, not columns. row_offset is the SAP row index, 7 is the column for Material.
                if (
                    str(materials[row]).lower() != 'nan'
                    and str(qty[row]).lower() != 'nan'
                    and str(unit[row]).lower() != 'nan'
                    and str(strloc[row]).lower() != 'nan'
                    ):
                    session.findById(f"wnd[0]/usr/sub:SAPMM07R:0521/ctxtRESB-MATNR[{row_offset},7]").text = materials[row] 
                    print("This: ",materials[row])
                    session.findById(f"wnd[0]/usr/sub:SAPMM07R:0521/txtRESB-ERFMG[{row_offset},48]").text = qty[row]
                    session.findById(f"wnd[0]/usr/sub:SAPMM07R:0521/ctxtRESB-ERFME[{row_offset},66]").text = unit[row]
                    session.findById(f"wnd[0]/usr/sub:SAPMM07R:0521/ctxtRESB-LGORT[{row_offset},76]").text = strloc[row]
                    session.findById('wnd[0]').sendVKey(0)
                    session.findById('wnd[0]').sendVKey(0)
            session.findById("wnd[0]/tbar[1]/btn[7]").press()
            idx += batch_size

            
        sys.exit()
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
        print(e)
        return jsonify({
            "status": "error",
            "error":  "SAP not Logged On OR Error while processing details check SAP to validate."
        }), 500




@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({
        "status": "ok",
        "message": "Server Running Successfully",
    }), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, port=5001, use_reloader = False) 
 
