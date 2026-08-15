import sqlite3
from database.database_manager import get_connection


def resolve_alert(alert_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(

        """

        UPDATE alerts

        SET status='Resolved'

        WHERE alert_id=?

        """,

        (alert_id,)

    )

    connection.commit()

    connection.close()