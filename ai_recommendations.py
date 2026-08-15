"""
=========================================================
Enterprise SOC Dashboard
AI Recommendation Engine
=========================================================
"""

from database.database_manager import get_connection


# ==========================================================
# Recommendation Dictionary
# ==========================================================

AI_RECOMMENDATIONS = {

    "ACL Denied": {
        "risk": "High",
        "recommendation": """
• Verify ACL configuration.
• Review source IP.
• Check firewall logs.
• Confirm unauthorized access attempt.
"""
    },

    "Port Scan Detected": {
        "risk": "Critical",
        "recommendation": """
• Block source IP immediately.
• Enable IDS/IPS monitoring.
• Review firewall traffic.
• Perform vulnerability assessment.
"""
    },

    "AAA Authentication Failure": {
        "risk": "High",
        "recommendation": """
• Verify user credentials.
• Check AAA Server.
• Review authentication logs.
• Reset compromised accounts if necessary.
"""
    },

    "Failed SSH Login": {
        "risk": "Medium",
        "recommendation": """
• Verify username.
• Check brute-force attempts.
• Review SSH logs.
• Enable account lockout policy.
"""
    },

    "Guest VLAN Access Attempt": {
        "risk": "High",
        "recommendation": """
• Guest Isolation working correctly.
• Verify ACL policy.
• Monitor repeated attempts.
"""
    },

    "Configuration Changed": {
        "risk": "Medium",
        "recommendation": """
• Review configuration backup.
• Verify administrator.
• Check audit logs.
"""
    },

    "Firewall NAT Translation": {
        "risk": "Low",
        "recommendation": """
• Normal Firewall Activity.
No action required.
"""
    },

    "DHCP Lease Assigned": {
        "risk": "Low",
        "recommendation": """
• DHCP working normally.
No action required.
"""
    },

    "DNS Query": {
        "risk": "Low",
        "recommendation": """
• DNS service operating normally.
"""
    },

    "Successful SSH Login": {
        "risk": "Low",
        "recommendation": """
• Authorized administrator login.
No action required.
"""
    }

}


# ==========================================================
# Get AI Recommendation
# ==========================================================

def get_ai_recommendation(event_name):

    return AI_RECOMMENDATIONS.get(

        event_name,

        {

            "risk": "Unknown",

            "recommendation": """
Review Security Logs.
Manual Investigation Required.
"""

        }

    )


# ==========================================================
# Display Recommendation
# ==========================================================

def display_ai_recommendation(event_name):

    recommendation = get_ai_recommendation(event_name)

    print("\n")

    print("=" * 60)

    print("AI INCIDENT RESPONSE")

    print("=" * 60)

    print("Event : ", event_name)

    print("Risk  : ", recommendation["risk"])

    print("\nRecommendation\n")

    print(recommendation["recommendation"])

    print("=" * 60)


# ==========================================================
# Save Recommendation to Alert
# ==========================================================

def update_alert_recommendation(alert_id, event_name):

    recommendation = get_ai_recommendation(event_name)

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        UPDATE alerts

        SET

        recommendation=?,

        risk=?

        WHERE alert_id=?

    """,

    (

        recommendation["recommendation"],

        recommendation["risk"],

        alert_id

    )

    )

    connection.commit()

    connection.close()


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    display_ai_recommendation("Port Scan Detected")