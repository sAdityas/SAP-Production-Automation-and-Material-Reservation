from connectSAP import connect_to_sap 
import time
from flask import jsonify


from orderNumber import OrderNumber 
from gotoCode import gotoCO11N
from enterOrderNumber import enterNumber
from flask import request, jsonify




def process_order(order_number, shift, quantity, operation_type, operation=None):

    session = connect_to_sap()
    gotoCO11N()

    enterNumber(order_number)
    
    time.sleep(0.5)
    
    count = 0
    process = []

    shell = session.findById("wnd[1]/usr/cntlCUSTOM_CONTAINER/shellcont/shell")
    row_count = shell.RowCount
    print(f"Total rows found: {row_count}")
    for i in range(row_count):
        try:
            time.sleep(0.2)
            # Read value from specific column (e.g., "VORNR" or "ARBPL" etc.)
            process_text = shell.GetCellValue(i, "F0001")  # <-- Change column name
            process.append(process_text)
            print(f"Row {i}: {process_text}")

        except Exception as e:
            print(f"Error on row {i}: {e}")
            continue



    # process = []
    # for i in range(50):
    #     try:
    #         time.sleep(0.2)
    #         shell = session.findById(f"wnd[1]/usr/sub/1[0]/sub/1/2[0]/sub/1/2/15[0,15]/lbl[1,{i}]")
    #         count += 1
    #         process.append(shell.Text)
    #     except Exception as e:
    #         # Element with this index does not exist
    #         print(e)
    #         break
    
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
            print(process[len(process) - 1])
            session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_HDR:SAPLCORU_S:0110/ctxtAFRUD-VORNR").setFocus()
            time.sleep(2)
            session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_HDR:SAPLCORU_S:0110/ctxtAFRUD-VORNR").caretPosition = 0
            session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_HDR:SAPLCORU_S:0110/ctxtAFRUD-VORNR").text = process[len(process) - 1]
            session.findById('wnd[0]').sendVKey(0)
        except Exception as e:
            print(e)
            is_last = True
            raise ValueError("Invalid operation type")

    elif operation_type=="B":
        try:
            print(operation)
            session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_HDR:SAPLCORU_S:0110/ctxtAFRUD-VORNR").setFocus()
            time.sleep(2)
            session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_HDR:SAPLCORU_S:0110/ctxtAFRUD-VORNR").caretPosition = 0
            session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_HDR:SAPLCORU_S:0110/ctxtAFRUD-VORNR").text = operation
            session.findById('wnd[0]').sendVKey(0)
         
        except:
            print()
            is_last = True
            raise ValueError("Invalid operation type")   
    
    qty_field = session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_DET1:SAPLCORU_S:0200/txtAFRUD-LMNGA")
    qty_field.setFocus()
    qty_field.text = quantity
    
    session.findById("wnd[0]").sendVKey(0)
    try:
        session.findById("wnd[1]").sendVKey(0)  
    except:
        pass

    shift_combo = session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_DET2:SAPLCORU_S:0910/subSLCUST:SAPLXCOF:0910/cmbAFRUD-SHIFT")
    print(f"[INFO] Setting shift to {shift}")
    shift_combo.key = shift
    
    session.findById("wnd[0]").sendVKey(0)
    try:
        session.findById("wnd[1]").sendVKey(0)  
    except:
        pass
    
    time.sleep(0.5)
    try:
        
        session.findById("wnd[0]").sendVKey(0)
        session.findById("wnd[0]/tbar[1]/btn[18]").setFocus()
        session.findById("wnd[0]/tbar[1]/btn[18]").press()
    except:
        session.findById("wnd[0]").sendVKey(0)
        session.findById("wnd[0]").sendVKey(18)
        session.findById("wnd[0]").sendVKey(18)
    
    time.sleep(0.5)

    if operation_type == 'A':
        time.sleep(0.5)
        session.findById("wnd[0]/usr/subPUSHBUTTON:SAPLCOWB:0400/btnMALL").press()
        time.sleep(0.5)
        session.findById("wnd[0]/usr/subTABLE:SAPLCOWB:0500/tblSAPLCOWBTCTRL_0500").getAbsoluteRow(0).selected = False
        session.findById("wnd[0]/usr/subTABLE:SAPLCOWB:0500/tblSAPLCOWBTCTRL_0500/ctxtCOWB_COMP-MATNR[0,0]").setFocus()
        session.findById("wnd[0]/usr/subPUSHBUTTON:SAPLCOWB:0400/btnCHFI").press()
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
    c = 0
    for i in range(50):
        materialCell = session.findById(f"wnd[0]/usr/subTABLE:SAPLCOWB:0500/tblSAPLCOWBTCTRL_0500/ctxtCOWB_COMP-MATNR[0,{i}]")
        if materialCell.Text == "" or materialCell.Text == None:
            break 
        materialCell.setFocus()
        c+= 1
    noBatchMat = []
    for i in range(0,c):
        print(c)
        batchCell = session.findById(f"wnd[0]/usr/subTABLE:SAPLCOWB:0500/tblSAPLCOWBTCTRL_0500/ctxtCOWB_COMP-CHARG[7,{i}]")
        if batchCell.Text == "" or batchCell.Text == None:
            batchCell.setFocus()
            noBatchMat.append(session.findById(f"wnd[0]/usr/subTABLE:SAPLCOWB:0500/tblSAPLCOWBTCTRL_0500/ctxtCOWB_COMP-MATNR[0,{i}]").text)
        else:
            pass
    print(len(noBatchMat))
    if len(noBatchMat) > 0:
        return {
            "status": "No Batch Material Found",
            "order_number": order_number,
            "operation": operation,
            "material" : noBatchMat
            }
    try:
        session.findById("wnd[0]/tbar[0]/btn[11]").press()
        session.findById("wnd[1]/usr/btnSPOP-OPTION2").press()
        session.findById("wnd[1]/usr/btnBUTTON_1").press()
        session.findById("wnd[1]/tbar[0]/btn[0]").press()
    except:
        session.findById("wnd[0]").sendVKey(11)
        session.findById("wnd[1]/usr/btnSPOP-OPTION2").press()
        session.findById("wnd[1]/usr/btnBUTTON_1").press()
