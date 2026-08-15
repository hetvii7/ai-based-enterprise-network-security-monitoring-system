import sqlite3

DATABASE_NAME = "database/enterprise_soc.db"

connection = sqlite3.connect(DATABASE_NAME)
cursor = connection.cursor()

print("=" * 60)
print("Populating Enterprise SOC Database...")
print("=" * 60)

# ==========================================================
# DEPARTMENTS
# ==========================================================

departments = [
    ("Admin", 10, "Administration Department"),
    ("HR", 20, "Human Resources"),
    ("IT", 30, "Information Technology"),
    ("Finance", 40, "Finance Department"),
    ("Production", 50, "Production Department"),
    ("Server Room", 60, "Enterprise Servers"),
    ("Guest WiFi", 70, "Guest Wireless Users")
]

cursor.executemany("""
INSERT OR IGNORE INTO departments
(department_name, vlan_id, description)
VALUES (?, ?, ?)
""", departments)

# ==========================================================
# VLANS
# ==========================================================

vlans = [
    (10, "ADMIN", "192.168.10.1", "192.168.10.0/24"),
    (20, "HR", "192.168.20.1", "192.168.20.0/24"),
    (30, "IT", "192.168.30.1", "192.168.30.0/24"),
    (40, "FINANCE", "192.168.40.1", "192.168.40.0/24"),
    (50, "PRODUCTION", "192.168.50.1", "192.168.50.0/24"),
    (60, "SERVERS", "192.168.60.1", "192.168.60.0/24"),
    (70, "GUEST_WIFI", "192.168.70.1", "192.168.70.0/24")
]

cursor.executemany("""
INSERT OR IGNORE INTO vlans
(vlan_id, vlan_name, gateway, subnet)
VALUES (?, ?, ?, ?)
""", vlans)

# ==========================================================
# DEVICES
# ==========================================================

devices = [
    ("Enterprise_Router", "Router", "10.0.0.1", "0001.42DE.0D01", 3, 30, "Online", "Main Rack"),
    ("EnterpriseFirewall", "ASA Firewall", "10.0.1.1", "000C.CF49.9003", 3, 30, "Online", "Main Rack"),
    ("Core_L3_Switch", "Layer 3 Switch", "10.0.1.2", "0060.47A0.CA01", 3, 30, "Online", "Main Rack"),
    ("AAA_Server", "AAA Server", "192.168.60.50", "AAAA.BBBB.C001", 6, 60, "Online", "Server Room"),
    ("DHCP_Server", "DHCP Server", "192.168.60.10", "AAAA.BBBB.C002", 6, 60, "Online", "Server Room"),
    ("DNS_Server", "DNS Server", "192.168.60.20", "AAAA.BBBB.C003", 6, 60, "Online", "Server Room"),
    ("Syslog_Server", "Syslog Server", "192.168.60.60", "AAAA.BBBB.C004", 6, 60, "Online", "Server Room"),
    ("NTP_Server", "NTP Server", "192.168.60.70", "AAAA.BBBB.C005", 6, 60, "Online", "Server Room")
]

cursor.executemany("""
INSERT OR IGNORE INTO devices
(hostname, device_type, ip_address, mac_address,
 department_id, vlan_id, status, location)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", devices)

# ==========================================================
# USERS
# ==========================================================

users = [
    ("admin", "Admin@123", "Network Administrator", 3),
    ("hetvi", "Hetvi@123", "Security Analyst", 3)
]

cursor.executemany("""
INSERT OR IGNORE INTO users
(username, password, role, department_id)
VALUES (?, ?, ?, ?)
""", users)

# ==========================================================
# SERVICES
# ==========================================================

services = [
    ("AAA", "Running"),
    ("DHCP", "Running"),
    ("DNS", "Running"),
    ("Syslog", "Running"),
    ("NTP", "Running"),
    ("SSH", "Running"),
    ("NAT", "Running")
]

cursor.executemany("""
INSERT OR IGNORE INTO services
(service_name, status)
VALUES (?, ?)
""", services)

# ==========================================================
# FIREWALL RULES
# ==========================================================

firewall_rules = [
    ("Inside", "Outside", "Permit", "IP", "Dynamic NAT"),
    ("Guest VLAN", "Finance VLAN", "Deny", "IP", "Guest Isolation"),
    ("LAN", "Internet", "Permit", "IP", "Default Internet Access")
]

cursor.executemany("""
INSERT OR IGNORE INTO firewall_rules
(source_ip, destination_ip, action, protocol, description)
VALUES (?, ?, ?, ?, ?)
""", firewall_rules)

# ==========================================================
# ACL RULES
# ==========================================================

acl_rules = [
    (100, "192.168.70.0/24", "192.168.60.20", "Permit", "DNS"),
    (100, "192.168.70.0/24", "192.168.60.30", "Permit", "HTTP"),
    (100, "192.168.70.0/24", "192.168.10.0/24", "Deny", "Admin VLAN"),
    (100, "192.168.70.0/24", "192.168.20.0/24", "Deny", "HR VLAN"),
    (100, "192.168.70.0/24", "192.168.30.0/24", "Deny", "IT VLAN"),
    (100, "192.168.70.0/24", "192.168.40.0/24", "Deny", "Finance VLAN"),
    (100, "192.168.70.0/24", "192.168.50.0/24", "Deny", "Production VLAN")
]

cursor.executemany("""
INSERT OR IGNORE INTO acl_rules
(acl_number, source, destination, action, description)
VALUES (?, ?, ?, ?, ?)
""", acl_rules)

# ==========================================================
# NETWORK HEALTH
# ==========================================================

cursor.execute("""
INSERT OR IGNORE INTO network_health
(cpu_usage, memory_usage, firewall_status,
 dhcp_status, dns_status, aaa_status,
 syslog_status, ntp_status, security_score)
VALUES (18, 42, 'Active',
        'Running', 'Running', 'Running',
        'Running', 'Running', 98)
""")

connection.commit()

print("\nDatabase populated successfully!")
connection.close()

print("=" * 60)
print("Enterprise SOC Data Ready")
print("=" * 60)