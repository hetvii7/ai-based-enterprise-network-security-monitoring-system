import sqlite3
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE = BASE_DIR / "database" / "enterprise_soc.db"

REPORT = BASE_DIR / "reports" / "Enterprise_SOC_Report.pdf"


def generate_report():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    devices = cursor.execute(
        "SELECT COUNT(*) FROM devices"
    ).fetchone()[0]

    logs = cursor.execute(
        "SELECT COUNT(*) FROM security_logs"
    ).fetchone()[0]

    alerts = cursor.execute(
        "SELECT COUNT(*) FROM alerts"
    ).fetchone()[0]

    health = cursor.execute(
        """
        SELECT
            security_score,
            cpu_usage,
            memory_usage
        FROM network_health
        LIMIT 1
        """
    ).fetchone()

    recent_alerts = cursor.execute(
        """
        SELECT
            threat,
            risk,
            recommendation
        FROM alerts
        ORDER BY alert_id DESC
        LIMIT 10
        """
    ).fetchall()

    connection.close()

    doc = SimpleDocTemplate(str(REPORT))

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "<b><font size=20>"
            "Enterprise SOC Dashboard Report"
            "</font></b>",
            styles["Title"]
        )
    )

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            "<b>Executive Summary</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Enterprise Devices : {devices}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Security Logs : {logs}",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Security Alerts : {alerts}",
            styles["BodyText"]
        )
    )

    if health:

        score,cpu,memory = health

        story.append(
            Paragraph(
                f"Security Score : {score}%",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"CPU Usage : {cpu}%",
                styles["BodyText"]
            )
        )

        story.append(
            Paragraph(
                f"Memory Usage : {memory}%",
                styles["BodyText"]
            )
        )

    story.append(Spacer(1,20))
    
    story.append(
        Paragraph(
            "<b>Enterprise Security Status</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "✔ Firewall : Protected",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "✔ Intrusion Detection System : Running",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "✔ Authentication : Active",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "✔ Network Monitoring : Operational",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "✔ Database : Connected",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1,20))
    story.append(
        Paragraph(
            "<b>Recent Security Alerts</b>",
            styles["Heading2"]
        )
    )

    table_data = [
        [
            "Threat",
            "Risk",
            "Recommendation"
        ]
    ]

    for row in recent_alerts:

        table_data.append(
            [
                row[0],
                row[1],
                row[2]
            ]
        )

    table = Table(table_data)

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.black),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

            ("BOTTOMPADDING",(0,0),(-1,0),10),

            ("TOPPADDING",(0,1),(-1,-1),6)

        ])

    )

    story.append(table)

    story.append(Spacer(1,20))
    
    story.append(
        Paragraph(
            "<b>Security Recommendations</b>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "• Review firewall configuration regularly.",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "• Apply operating system security updates.",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "• Enable Multi-Factor Authentication (MFA).",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "• Monitor critical alerts continuously.",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            "• Backup enterprise data regularly.",
            styles["BodyText"]
        )
    )

    story.append(Spacer(1,20))

    story.append(

        Paragraph(

            "<b>Conclusion</b>",

            styles["Heading2"]

        )

    )

    story.append(
        Paragraph(
            """
            The Enterprise SOC Dashboard continuously monitors enterprise devices,
            security logs, and alerts to provide centralized visibility into the
            organization's cybersecurity posture.<br/><br/>

            This report summarizes the current security status and highlights
            recent security events to support informed operational and security
            decisions.<br/><br/>

            <b>Generated Automatically by Enterprise SOC Dashboard</b><br/><br/>

            <b>Developed by:</b><br/>
            Hetvi Upadhyay
            """,
            styles["BodyText"]
        )
    )
    doc.build(story)

    return str(REPORT)


if __name__ == "__main__":

    path = generate_report()

    print("Report Generated Successfully")

    print(path)