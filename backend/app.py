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

        # shell = session.findById("wnd[1]/usr/cntlCUSTOM_CONTAINER/shellcont/shell")
        # row_count = shell.RowCount
        # print(f"Total rows found: {row_count}")
        # for i in range(row_count):
        #     try:
        #         time.sleep(0.2)
        #         process_text = shell.GetCellValue(i, "F0001")  # <-- Change column name
        #         ops.append(process_text)
        #         print(f"Row {i}: {process_text}")

        #     except Exception as e:
        #         print(f"Error on row {i}: {e}")
        #         continue

        # Close the popup
        # session.findById("wnd[1]/tbar[0]/btn[12]").press()
        
        try:
            count=0
            for i in range(3,50): 
                    shell = session.findById(f"wnd[1]/usr/sub/1[0]/sub/1/2[0]/sub/1/2/15[0,15]/lbl[1,{i}]")
                    shell.setFocus()
                    ops.append(shell.Text)
                    print(ops)
                    count += 1
        except Exception as e:
            print(f'for loop ended {e}  ')
        # Close the popup
        session.findById("wnd[1]/tbar[0]/btn[12]").press()
        return jsonify({"operations": ops}), 200
    
    
    except Exception as e:
        print(e)
        return jsonify({"error": "Error while getting Operations check SAP."}), 500

@app.route("/btchdtr", methods=["POST"])
def btchDtr():
    try:
        mvmt = '311'
        plant = '1002'
        file = request.files.get("file")

        if not file:
            return jsonify({'error': 'File is required'}), 400

        if not file.filename.endswith('.csv'):
            return jsonify({
                'error': 'Only CSV files are supported',
                "status": "failed",
                "plant": plant
            }), 400

        df = pd.read_csv(file)

        materials = df['Material'].astype(str).tolist()
        qty       = df['Quantity'].astype(str).tolist()
        unit      = df['UnE'].astype(str).tolist()
        recloc    = df['Receiving Location'].astype(str).tolist()
        strloc    = df['Storage Location'].astype(str).tolist()

        print(f"[INFO] Processing {len(materials)} materials for plant {plant}")

        # Connect to SAP
        session =connect_to_sap()
        session.findById("wnd[0]").maximize()
        session.findById("wnd[0]/tbar[0]/okcd").text = "/nMB21"
        session.findById("wnd[0]").sendVKey(0)
        time.sleep(0.5)

        # Enter Movement Type & Plant
        mvmtfield = session.findById("wnd[0]/usr/ctxtRM07M-BWART")
        if mvmtfield:
            mvmtfield.text = mvmt

        plantfield = session.findById("wnd[0]/usr/ctxtRM07M-WERKS")
        if plantfield:
            plantfield.text = plant

        time.sleep(0.8)
        session.findById("wnd[0]").sendVKey(0)

        # Receiving location for all rows
        session.findById("wnd[0]/usr/ctxtRKPF-UMLGO").text = recloc[0]

        total_materials = len(materials)
        batch_size = 14
        idx = 0

        row_errors = []   # store row-level errors

        # ---------------------------
        #   MAIN ROW INSERT LOOP
        # ---------------------------
        while idx < total_materials:
            end_idx = min(idx + batch_size, total_materials)

            for row in range(idx, end_idx):
                row_offset = row - idx  # index inside SAP table (0–13)

                # Build SAP field paths
                mat_path   = f"wnd[0]/usr/sub:SAPMM07R:0521/ctxtRESB-MATNR[{row_offset},7]"
                qty_path   = f"wnd[0]/usr/sub:SAPMM07R:0521/txtRESB-ERFMG[{row_offset},48]"
                unit_path  = f"wnd[0]/usr/sub:SAPMM07R:0521/ctxtRESB-ERFME[{row_offset},66]"
                lgort_path = f"wnd[0]/usr/sub:SAPMM07R:0521/ctxtRESB-LGORT[{row_offset},76]"

                try:
                    # -------------------------------
                    # FILL THIS ROW
                    # -------------------------------
                    session.findById(mat_path).text = materials[row]
                    session.findById(qty_path).text = qty[row]
                    session.findById(unit_path).text = unit[row]
                    session.findById(lgort_path).text = strloc[row]

                    # Trigger SAP validation (your "enter" twice)
                    session.findById("wnd[0]").sendVKey(0)
                    session.findById("wnd[0]").sendVKey(0)

                    # -----------------------------------------
                    # CHECK STATUS BAR → DID SAP REJECT INPUT?
                    # -----------------------------------------
                    status_bar = session.findById("wnd[0]/sbar")
                    msg_type = getattr(status_bar, "MessageType", "")
                    msg_text = getattr(status_bar, "Text", "")

                    # If message type is Error or Abort, this row failed
                    if msg_type in ("E", "A"):
                        print(f"[ROW ERROR] Row {row} failed: {msg_text}")
                        row_errors.append({
                            "row": row,
                            "material": materials[row],
                            "error": msg_text
                        })

                        # Clear the row to be safe
                        try:
                            session.findById(mat_path).text = ""
                            session.findById(qty_path).text = ""
                            session.findById(unit_path).text = ""
                            session.findById(lgort_path).text = ""
                            session.findById("wnd[0]").sendVKey(0)
                        except Exception as cleanup_err:
                            print(f"[WARN] Could not clear row {row}: {cleanup_err}")


                        # Continue to next row
                        continue

                except Exception as script_err:
                    # Unexpected script issue (element missing, etc.)
                    print(f"[SCRIPT ERROR] Row {row} failed: {script_err}")
                    try:
                        session.findById(mat_path).text = ""
                        session.findById(qty_path).text = ""
                        session.findById(unit_path).text = ""
                        session.findById(lgort_path).text = ""
                        session.findById("wnd[0]").sendVKey(0)
                    except Exception as cleanup_err:
                        print(f"[WARN] Could not clear row {row} after script error: {cleanup_err}")
                    if '<unknown>.text' not in str(script_err):
                        row_errors.append({
                            "row": row,
                            "material": materials[row],
                            "error": str(script_err)
                        })
                    continue

            # Go to next SAP page
            session.findById("wnd[0]/tbar[1]/btn[7]").press()
            idx += batch_size

        # ---------------------------
        # SAVE DOCUMENT
        # ---------------------------
        session.findById("wnd[0]/tbar[0]/btn[11]").press()
        time.sleep(2)

        status_text = session.findById("wnd[0]/sbar").Text
        doc_number = None

        for word in status_text.split():
            if word.isdigit() and len(word) >= 10:
                doc_number = word
                break

        message = f"Material reservation created. Document: {doc_number}"

        response = {
            "status": "success",
            "mvmt": mvmt,
            "plant": plant,
            "message": message,
            "row_errors": row_errors  # keeps output of failed rows
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({
        "status": "ok",
        "message": "Server Running Successfully",
    }), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True, port=5001) 
 
