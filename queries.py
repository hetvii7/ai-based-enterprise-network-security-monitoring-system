from database_manager import fetch_all

tables = [
    "departments",
    "vlans",
    "devices",
    "users",
    "services",
    "firewall_rules",
    "acl_rules",
    "network_health"
]

for table in tables:

    print("\n" + "=" * 70)
    print(f"{table.upper()}")
    print("=" * 70)

    rows = fetch_all(f"SELECT * FROM {table}")

    if not rows:
        print("No Records Found")
        continue

    for row in rows:
        print(dict(row))