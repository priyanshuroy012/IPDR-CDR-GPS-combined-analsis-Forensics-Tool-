# IPDR Integration Module – DIFA (Digital Investigator for Android)

The **IPDR (Internet Protocol Detail Record) Integration Module** is part of the **DIFA** forensic suite.  
It allows investigators to **ingest, process, and correlate IPDR data** with GPS and CDR records to identify suspicious network activity, location mismatches, and behavioral anomalies.

---

## 📌 Overview
IPDR records contain detailed metadata about internet usage sessions from telecom operators.  
When combined with **GPS** and **CDR** data, the module can:
- Map user activity across **time, network, and location** dimensions.
- Detect possible **SIM swaps, IP spoofing, and abnormal travel patterns**.
- Correlate internet activity with **physical presence** for investigative leads.

---

## 🚀 Features
- **Multi-source Integration**  
  Load and merge IPDR data with GPS and CDR datasets.
  
- **Anomaly Detection**  
  Uses Isolation Forest and Autoencoder ML models to detect:
  - Impossible travel distances between logins.
  - Multiple IP addresses from different regions in short intervals.
  - Mismatches between GPS location and IP geolocation.

- **Visualization**  
  Interactive timeline & map for:
  - Session start/end times.
  - IP location plotting.
  - Behavioral profile clusters.

- **Forensic Output**  
  - Highlighted suspicious events.
  - Exportable CSV & unified PDF report integration.

---

## 📂 Input Format
**CSV Columns** (Required):
```text
timestamp, ip_address, port, session_duration, device_id, imsi, imei




🛠 How It Works
Data Loading – Upload IPDR CSV or extract from device image via DIFA's evidence handler.

Integration – Merge with GPS & CDR datasets.

Anomaly Analysis – Apply ML and rule-based checks.

Visualization – Render interactive map and timeline.

Reporting – Send anomalies to the unified DIFA report.

🧠 Algorithms Used
Isolation Forest (Sklearn) – Detect statistical outliers in geolocation and IP changes.

Autoencoder (Keras/TensorFlow) – Detect deviations from normal behavior patterns.

GeoIP Lookup – Map IP addresses to physical locations.

Haversine Distance – Calculate distance between GPS points to flag impossible travel.

📊 Outputs
Interactive session map with cluster-based color coding.

Anomaly table with:

Timestamp

IP address & geolocation

Risk classification (Low / Medium / High)

Export to CSV, JSON, or unified PDF.

📜 Example Use Case
An investigator uploads an IPDR log and GPS data from a suspect's device. The system detects that on the same day:

GPS shows location in Delhi

IP geolocation points to Singapore

Travel gap is < 5 minutes
The system flags this as a probable VPN/proxy use or account compromise.

📦 Installation & Usage
This module is part of DIFA and not intended for standalone deployment.

Inside DIFA:

streamlit run app.py
# Select IPDR Integration from module drawer
📄 License
MIT License – see LICENSE for details.

yaml









