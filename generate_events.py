import random
from datetime import datetime

from database.database_manager import get_connection
from event_generator.event_types import EVENTS


# ==========================================================
# Get Random Device
# ==========================================================

def get_random_device():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT device_id,
               hostname,
               ip_address
        FROM devices
    """)

    devices = cursor.fetchall()

    connection.close()

    if len(devices) == 0:
        raise Exception("No devices found in database.")

    return random.choice(devices)


# ==========================================================
# AI Recommendation
# ==========================================================

def get_recommendation(event_name):

    recommendations = {

        "ACL Denied":
        "Verify ACL rules and investigate unauthorized access attempt.",

        "Successful SSH Login":
        "Normal administrative login detected.",

        "Failed SSH Login":
        "Check user credentials and investigate repeated failures.",

        "Firewall NAT Translation":
        "Normal firewall NAT operation.",

        "DHCP Lease Assigned":
        "Normal DHCP service activity.",

        "DNS Query":
        "Normal DNS request observed.",

        "Port Scan Detected":
        "Immediately investigate source IP and consider blocking it.",

        "Guest VLAN Access Attempt":
        "Guest isolation working correctly. Verify if repeated attempts occur.",

        "Configuration Changed":
        "Review configuration changes and validate authorization.",

        "AAA Authentication Failure":
        "Verify AAA server logs and authentication credentials."

    }

    return recommendations.get(
        event_name,
        "Review security logs."
    )


# ==========================================================
# Generate Event
# ==========================================================

def generate_event():

    device = get_random_device()

    event = random.choice(EVENTS)

    destination_ips = [

        "192.168.10.1",
        "192.168.20.1",
        "192.168.30.1",
        "192.168.40.1",
        "192.168.50.1",
        "192.168.60.1",
        "8.8.8.8",
        "1.1.1.1"

    ]

    destination_ip = random.choice(destination_ips)

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""

        INSERT INTO security_logs

        (

            timestamp,

            source_ip,

            destination_ip,

            event_type,

            severity,

            action,

            device_id

        )

        VALUES

        (?, ?, ?, ?, ?, ?, ?)

    """,

    (

        datetime.now(),

        device["ip_address"],

        destination_ip,

        event["event"],

        event["severity"],

        event["action"],

        device["device_id"]

    )

    )

    log_id = cursor.lastrowid

    if event["severity"] in ["High", "Critical"]:

        cursor.execute("""

            INSERT INTO alerts

            (

                log_id,

                threat,

                risk,

                recommendation,

                status

            )

            VALUES

            (?, ?, ?, ?, ?)

        """,

        (

            log_id,

            event["event"],

            event["severity"],

            get_recommendation(event["event"]),

            "Open"

        )

        )

    connection.commit()

    connection.close()

    print()

    print("=" * 65)

    print("ENTERPRISE SOC EVENT GENERATED")

    print("=" * 65)

    print(f"Time           : {datetime.now()}")

    print(f"Device         : {device['hostname']}")

    print(f"Source IP      : {device['ip_address']}")

    print(f"Destination IP : {destination_ip}")

    print(f"Event          : {event['event']}")

    print(f"Severity       : {event['severity']}")

    print(f"Action         : {event['action']}")

    print("=" * 65)

    print()


# ==========================================================
# Main
# ==========================================================

if __name__ == "__main__":

    generate_event()