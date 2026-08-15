import sqlite3

# ==========================================================
# Enterprise SOC Dashboard Database Creation
# ==========================================================

DATABASE_NAME = "database/enterprise_soc.db"

connection = sqlite3.connect(DATABASE_NAME)
cursor = connection.cursor()

# Enable Foreign Keys
cursor.execute("PRAGMA foreign_keys = ON")

print("=" * 60)
print("Creating Enterprise SOC Database...")
print("=" * 60)

# ==========================================================
# DEPARTMENTS
# ==========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT NOT NULL UNIQUE,
    vlan_id INTEGER NOT NULL UNIQUE,
    description TEXT
)
""")

# ==========================================================
# VLANS
# ==========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS vlans (
    vlan_id INTEGER PRIMARY KEY,
    vlan_name TEXT NOT NULL,
    gateway TEXT NOT NULL,
    subnet TEXT NOT NULL
)
""")

# ==========================================================
# DEVICES
# ==========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS devices (
    device_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hostname TEXT NOT NULL,
    device_type TEXT NOT NULL,
    ip_address TEXT NOT NULL UNIQUE,
    mac_address TEXT,
    department_id INTEGER,
    vlan_id INTEGER,
    status TEXT,
    location TEXT,

    FOREIGN KEY (department_id)
        REFERENCES departments(department_id),

    FOREIGN KEY (vlan_id)
        REFERENCES vlans(vlan_id)
)
""")

# ==========================================================
# USERS
# ==========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT,
    role TEXT,
    department_id INTEGER,

    FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
)
""")

# ==========================================================
# SERVICES
# ==========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS services (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL
)
""")

# ==========================================================
# FIREWALL RULES
# ==========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS firewall_rules (
    rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_ip TEXT,
    destination_ip TEXT,
    action TEXT,
    protocol TEXT,
    description TEXT
)
""")

# ==========================================================
# ACL RULES
# ==========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS acl_rules (
    acl_id INTEGER PRIMARY KEY AUTOINCREMENT,
    acl_number INTEGER,
    source TEXT,
    destination TEXT,
    action TEXT,
    description TEXT
)
""")

# ==========================================================
# SECURITY LOGS
# ==========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS security_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    source_ip TEXT,
    destination_ip TEXT,
    event_type TEXT,
    severity TEXT,
    action TEXT,
    device_id INTEGER,

    FOREIGN KEY (device_id)
        REFERENCES devices(device_id)
)
""")

# ==========================================================
# ALERTS
# ==========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS alerts (
    alert_id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_id INTEGER,
    threat TEXT,
    risk TEXT,
    recommendation TEXT,
    status TEXT,

    FOREIGN KEY (log_id)
        REFERENCES security_logs(log_id)
)
""")

# ==========================================================
# AUDIT LOGS
# ==========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS audit_logs (
    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    username TEXT,
    activity TEXT
)
""")

# ==========================================================
# NETWORK HEALTH
# ==========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS network_health (
    health_id INTEGER PRIMARY KEY AUTOINCREMENT,
    cpu_usage REAL,
    memory_usage REAL,
    firewall_status TEXT,
    dhcp_status TEXT,
    dns_status TEXT,
    aaa_status TEXT,
    syslog_status TEXT,
    ntp_status TEXT,
    security_score INTEGER
)
""")

# ==========================================================
# REPORTS
# ==========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (
    report_id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_name TEXT,
    generated_on DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# ==========================================================
# SAVE CHANGES
# ==========================================================

connection.commit()

print("\nDatabase Created Successfully!\n")

# Display all tables
tables = cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
""").fetchall()

print("Tables Created:\n")

for table in tables:
    print("[OK]", table[0])

connection.close()

print("\n" + "=" * 60)
print("Enterprise SOC Database Ready")
print("=" * 60)