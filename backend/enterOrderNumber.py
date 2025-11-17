import time
from connectSAP import connect_to_sap


def enterNumber(order_number):

    session = connect_to_sap()
    session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_HDR:SAPLCORU_S:0110/ctxtAFRUD-AUFNR").text = order_number
    session.findById("wnd[0]/usr/ssubSUB01:SAPLCORU_S:0010/subSLOT_HDR:SAPLCORU_S:0110/ctxtAFRUD-VORNR").setFocus()
    session.findById("wnd[0]").sendVKey (4)