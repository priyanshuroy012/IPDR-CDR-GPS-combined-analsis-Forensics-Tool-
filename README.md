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
