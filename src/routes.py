import datetime

from dotenv import load_dotenv
from loguru import logger
from typing import List, Optional, Tuple

from database.connect import connect_database


def close_connect(connection, cursor):
    logger.info("Close cursor success")
    cursor.close()
    logger.info("Close connection success")
    connection.close()


def fertilizer_get_handler() -> Tuple[Optional[List], Optional[Exception]]:
    try:
        load_dotenv()
        connection = connect_database()
        if connection is None:
            return
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM fertilizer")
        data = cursor.fetchall()

        close_connect(connection, cursor)

        return data, None
    except Exception as e:
        return None, e


def fertilizer_insert_handler(information) -> Optional[Exception]:
    try:
        load_dotenv()
        connection = connect_database()
        currentDateTime = datetime.datetime.now()
        cursor = connection.cursor()

        insertQuery = """INSERT INTO fertilizer VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        cursor.execute(insertQuery,
                       (information[0], "公斤", information[1],
                        information[2], information[3], information[4], currentDateTime))
        connection.commit()

        close_connect(connection, cursor)

        return None
    except Exception as e:
        return e
