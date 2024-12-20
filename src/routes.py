from dotenv import load_dotenv
from loguru import logger
from typing import List, Optional, Tuple

from database.connect import connect_database


def fertilizerHandler() -> Tuple[Optional[List], Optional[Exception]]:
    try:
        load_dotenv()
        connection = connect_database()
        if connection is None:
            return
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM fertilizer")
        data = cursor.fetchall()

        logger.info("Close cursor success")
        cursor.close()
        logger.info("Close connection success")
        connection.close()

        return data, None
    except Exception as e:
        return None, e
