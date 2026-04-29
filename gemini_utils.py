import os
import google.generativeai as genai

# Configure API
genai.configure(api_key="AIzaSyA45OZ0ft-P61c9VWVZj8hmy3D3cUUovnU")

# Load model
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_forensic_explanation(anomaly):
    """
    anomaly: dict containing anomaly details
    returns: AI-generated explanation
    """

    prompt = f"""
    You are a digital forensic analyst.

    Analyze the following anomaly and provide:
    1. What happened
    2. Why it is suspicious
    3. Possible causes (VPN, SIM swap, spoofing, compromise, etc.)
    4. Risk level (Low/Medium/High)
    5. Recommended investigator action

    Anomaly Data:
    Timestamp: {anomaly.get('timestamp')}
    IP Address: {anomaly.get('ip_address')}
    IP Location: {anomaly.get('ip_location')}
    GPS Location: {anomaly.get('gps_location')}
    Distance: {anomaly.get('distance')}
    Time Gap: {anomaly.get('time_gap')}
    Device ID: {anomaly.get('device_id')}
    IMSI: {anomaly.get('imsi')}
    IMEI: {anomaly.get('imei')}
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating explanation: {str(e)}"