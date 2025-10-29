import win32com.client
import pythoncom

def connect_to_sap():
    pythoncom.CoInitialize()  # Initialize COM library for this thread
    try:
        SapGuiAuto = win32com.client.GetObject("SAPGUI")
        application = SapGuiAuto.GetScriptingEngine
        connection = application.Children(0)
        session = connection.Children(0)
        print("[INFO] Connected to SAP session.")
        
        return session
    except Exception as e:
        raise ConnectionError(f"Could not connect to SAP GUI: ")