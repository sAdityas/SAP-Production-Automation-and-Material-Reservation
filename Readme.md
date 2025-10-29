# 🚀 SAP Production Automation and Material Reservation

This project automates key **SAP Production (PP)** and **Material Reservation (MM)** processes using **Python** and the **SAP GUI Scripting API**.  
It enables hands-free execution of repetitive SAP T-Codes such as **CO11N**, **VL01N**, and **MB21**, reducing manual effort and human error.

---

## 🧠 Overview

SAP automation is designed to:
- Automate confirmation of production orders (CO11N)
- Reserve materials automatically based on production requirements
- Generate, process, and validate operations dynamically
- Integrate with Excel/CSV files for data-driven automation
- Allow both **manual** and **automatic** operation selection modes

---

## ⚙️ Features

✅ **Automated Production Order Confirmation (CO11N)**  
✅ **Dynamic Material Reservation (MB21 / VL01N)**  
✅ **Excel-based input for batch processing**  
✅ **Error handling & logging for failed transactions**  
✅ **Supports both single & multi-operation orders**  
✅ **Looped processing with real-time SAP GUI interaction**  
✅ **Modular Python design for reusability (`sap_processor.py`)**

---

## 🧩 Project Structure
```
SAP-Production-Automation-and-Material-Reservation/
│
├── Material Reservation with CSV/
│   ├── Book1.csv                # Example CSV for material reservation
│   ├── ProcessOrder.py          # Main SAP automation logic for CO11N
│   ├── app.py                   # Flask API backend server
│   ├── connectSAP.py            # SAP GUI connection setup
│   ├── enterOrderNumber.py      # Logic to enter production order number
│   ├── gotoCode.py              # Function to navigate to CO11N transaction
│   ├── orderNumber.py           # Helper functions for order management
│   └── test.py                  # Testing and debugging scripts
│
└── frontend/
    ├── public/                  # Static assets for React app
    └── src/
        ├── App.css              # Global styles
        ├── App.jsx              # Root React component
        ├── App.test.js          # Jest test file
        ├── Batch.jsx            # Component for Material Reservation page
        ├── PrdOrder.jsx         # Component for Production Order Confirmation page
        ├── index.css            # Base styling
        └── index.js             # React DOM entry point

```

## 🖥️ Tech Stack

| Layer | Technology |
|-------|-------------|
| Backend | Python (Flask / FastAPI) |
| SAP Automation | SAP GUI Scripting API |
| Frontend | React (with Axios) |
| Data | Excel / CSV |
| Authentication | JWT / LocalStorage |
| Hosting (optional) | GitHub / Localhost |

---

## ⚡ Quick Start

### 1️⃣ Prerequisites
- Windows OS with **SAP GUI** installed  
- **SAP Scripting** enabled (`RZ11` → `sapgui/user_scripting = TRUE`)
- Python 3.10+  
- Access to target SAP system

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 3️⃣ Run Backend
```bash
python main.py
```

Server runs at → http://localhost:5050

### 4️⃣ Run Frontend
```bash
npm install
npm start
```


Frontend runs at → http://localhost:3000

# 🔁 Example Workflow

Upload Excel file containing Production Order Numbers

Script logs into SAP automatically

Launches CO11N transaction

Iterates through operations & confirms quantities

Creates Material Reservations if required (MB21)

Logs results & status to Excel or console

# 🧠 Key Python Functions

launch_transaction(code) → Opens SAP T-code

extract_operations() → Reads operations dynamically from popup

confirm_operation(order, qty, shift) → Confirms operation

reserve_materials(order) → Creates reservation document

log_results() → Writes success/failure logs

# 🔒 Security Notes

Never commit your SAP credentials or tokens to GitHub.

Use .env file or Windows Credential Manager for sensitive data.

# 📄 License

This project is licensed under the MIT License — free for personal and commercial use.

### 👨‍💻 Author Aditya Sarkale
### 💼 GitHub: @sAdityas
### 💡 Passionate about SAP automation, integration, and AI-driven process optimization.
