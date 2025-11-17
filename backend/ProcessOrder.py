from connectSAP import connect_to_sap 
import time
from flask import jsonify
import sys

from gotoCode import gotoCO11N
from enterOrderNumber import enterNumber
from getStatusText import status_text





def process_order(order_number, shift, quantity, operation_type, operation=None):

    # Get the session variable 
    session = connect_to_sap()

    # Go to CO11N T-Code
    gotoCO11N()

    # Go to Enter Order Number    
    enterNumber(order_number)
    
    time.sleep(0.2)
    
    count = 0

    ''' THIS IS FOR DEVELELOPMENT PURPOSE ONLY TO GET OPERATION LIST '''
    # Getting the Shell to count the rows and get operation
    # shell = session.findById("wnd[1]/usr/cntlCUSTOM_CONTAINER/shellcont/shell")
    # row_count = shell.RowCount
    # print(f"Total rows found: {row_count}")
    # for i in range(row_count):
    #     try:
    #         time.sleep(0.2)
    #         process_text = shell.GetCellValue(i, "F0001") 
    #         process.append(process_text)
    #         print(f"Row {i}: {process_text}")

    #     except Exception as e:
    #         print(f"Error on row {i}: {e}")
    #         continue


    """ THIS IS FOR PRODUCTION PURPOSE TO GET OPERATION LIST """
    # process = []
    for i in range(3,50):
        try:
            time.sleep(0.2)
            shell = session.findById(f"wnd[1]/usr/sub/1[0]/sub/1/2[0]/sub/1/2/15[0,15]/lbl[1,{i}]")
            shell.setFocus()
            count += 1
        except Exception as e:
            # Element with this index does not exist
            break

    session.findById("wnd[1]/tbar[0]/btn[12]").press()
        
    # Look for last row

    row_count = count
    print(row_count)
    last_row = row_count
    first_row = 0
    print(f"[INFO] Last row: {last_row}, First row: {first_row}")

    # Operation TYPE
    if operation_type == 'A':
        if row_count == 0:
            raise ValueError("No operations found in the order.")
        last_row = count
        try:
            sys.exit()
            session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_HDR:SAPLCORU_S:0110/ctxtAFRUD-VORNR").setFocus()
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
            session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_HDR:SAPLCORU_S:0110/ctxtAFRUD-VORNR").caretPosition = 0
            session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_HDR:SAPLCORU_S:0110/ctxtAFRUD-VORNR").text = operation
            session.findById('wnd[0]').sendVKey(0)
         
        except:
            is_last = True
            raise ValueError("Invalid operation type")   
    # Setting Qty

    qty_field = session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_DET1:SAPLCORU_S:0200/txtAFRUD-LMNGA")
    qty_field.setFocus()
    qty_field.text = quantity
    
    session.findById("wnd[0]").sendVKey(0)
    try:
        session.findById("wnd[1]").sendVKey(0)  
    except:
        pass
    
    # Setting Shift
    shift_combo = session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_DET2:SAPLCORU_S:0910/subSLCUST:SAPLXCOF:0910/cmbAFRUD-SHIFT")
    print(f"[INFO] Setting shift to {shift}")
    shift_combo.key = shift
    
    session.findById("wnd[0]").sendVKey(0)
    try:
        session.findById("wnd[1]").sendVKey(0)  
    except:
        pass
    time.sleep(0.2)
    try:
        session.findById("wnd[0]").sendVKey(0)
        session.findById("wnd[0]/tbar[1]/btn[18]").setFocus()
        session.findById("wnd[0]/tbar[1]/btn[18]").press()
    except:
        session.findById("wnd[0]").sendVKey(0)
        session.findById("wnd[0]").sendVKey(18)
        session.findById("wnd[0]").sendVKey(18)
    time.sleep(0.2)

    # Operation Type

    if operation_type == 'A':
        time.sleep(0.2)
        session.findById("wnd[0]/usr/subPUSHBUTTON:SAPLCOWB:0400/btnMALL").press()
        time.sleep(0.2)
        session.findById("wnd[0]/usr/subTABLE:SAPLCOWB:0500/tblSAPLCOWBTCTRL_0500").getAbsoluteRow(0).selected = False
        session.findById("wnd[0]/usr/subTABLE:SAPLCOWB:0500/tblSAPLCOWBTCTRL_0500/ctxtCOWB_COMP-MATNR[0,0]").setFocus()
       
        time.sleep(0.2)
    elif operation_type == 'B':
        time.sleep(0.2)
        session.findById("wnd[0]/usr/subPUSHBUTTON:SAPLCOWB:0400/btnMALL").press()
        time.sleep(0.2)
    elif operation_type == 'B' and is_last:
        time.sleep(0.2)
        session.findById("wnd[0]/usr/subPUSHBUTTON:SAPLCOWB:0400/btnMALL").press()
        time.sleep(0.2)
        session.findById("wnd[0]/usr/subTABLE:SAPLCOWB:0500/tblSAPLCOWBTCTRL_0500").getAbsoluteRow(0).selected = False
        session.findById("wnd[0]/usr/subTABLE:SAPLCOWB:0500/tblSAPLCOWBTCTRL_0500/ctxtCOWB_COMP-MATNR[0,0]").setFocus()
    time.sleep(0.2)

    # Count Variable
    c = 0

    # Batch Determination

    session.findById("wnd[0]/usr/subPUSHBUTTON:SAPLCOWB:0400/btnCHFI").press()

    # Status Bar Text
    try:
        errorMessage = status_text()
    except:
        pass
    
    # Count if materials
    for i in range(50):
        materialCell = session.findById(f"wnd[0]/usr/subTABLE:SAPLCOWB:0500/tblSAPLCOWBTCTRL_0500/ctxtCOWB_COMP-MATNR[0,{i}]")
        if materialCell.Text == "" or materialCell.Text == None:
            break 
        materialCell.setFocus()
        c+= 1

    # No batch Material Array
    noBatchMat = []

    # Appending in to the Array
    for i in range(1,c):
        batchCell = session.findById(f"wnd[0]/usr/subTABLE:SAPLCOWB:0500/tblSAPLCOWBTCTRL_0500/ctxtCOWB_COMP-CHARG[7,{i}]")
        if batchCell.Text == "" or batchCell.Text == None:  
            batchCell.setFocus()
            noBatchMat.append(session.findById(f"wnd[0]/usr/subTABLE:SAPLCOWB:0500/tblSAPLCOWBTCTRL_0500/ctxtCOWB_COMP-MATNR[0,{i}]").text)
        else:
            pass
    # Return if there is no btach material
    if len(noBatchMat) > 0:
        return {
            "status": "failed",
            "order_number": order_number,
            "operation": operation if operation else None,
            "material" : noBatchMat,
            "msg" : errorMessage or "Material with no Batch Found"
            }
    try:
        session.findById("wnd[0]/tbar[0]/btn[11]").press()
        session.findById("wnd[1]/usr/btnSPOP-OPTION2").press()
        session.findById("wnd[1]/usr/btnBUTTON_1").press()
        session.findById("wnd[1]/tbar[0]/btn[0]").press()
    except:
        pass

    return {
        "status" : "success",
        "operation": operation if operation else None,
        "order_number" : order_number
        }