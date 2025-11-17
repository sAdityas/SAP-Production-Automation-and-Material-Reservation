from connectSAP import connect_to_sap
import time


def status_text():
    session = connect_to_sap()
    print("IN STATUS BAR TEXT")
    time.sleep(1)
    
    status_bar_text = session.findById("wnd[0]/sbar").text
    print("STATUS BAR TEXT:", status_bar_text)

    # Check if specific phrase or keyword exists
    if "batches" in status_bar_text.lower() or \
       "no batches/stocks were found" in status_bar_text.lower():
        print("Batch message detected, closing window...")
        session.findById("wnd[0]/tbar[0]/btn[3]").press()
        return "Batch not found"

    return status_bar_text

        