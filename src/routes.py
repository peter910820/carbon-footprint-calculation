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
        cursor = connection.cursor()
        currentDateTime = datetime.datetime.now()

        insertQuery = """INSERT INTO fertilizer VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        cursor.execute(insertQuery,
                       (information[0], "公斤", information[1],
                        information[2], information[3], information[4], currentDateTime))

        connection.commit()
        close_connect(connection, cursor)
        return None
    except Exception as e:
        return e


def product_insert_handler(information, information_fertilizer, information_dosage_fertilizer) -> Optional[Exception]:
    try:
        load_dotenv()
        connection = connect_database()
        cursor = connection.cursor()
        currentDateTime = datetime.datetime.now()
        fertilizer, dosage_fertilizer = '', ''
        fertilizer_insert, total_co2e = "", 0.0
        fertilizer_integrate = []
        translate = {"urea": "尿素",
                     "superphosphate": "過磷酸鈣",
                     "potassium_chloride": "氯化鉀",
                     "calcium_ammonium_nitrate": "硝酸銨鈣(肥料用)"}

        for f in information_fertilizer:
            fertilizer += f"{f}//"
        for d_f in information_dosage_fertilizer:
            dosage_fertilizer += f"{d_f}//"
        fertilizer_integrate.append(fertilizer)
        fertilizer_integrate.append(dosage_fertilizer)

        fertilizer_name = fertilizer_integrate[0].split("//")
        fertilizer_dosage = fertilizer_integrate[1].split("//")
        fertilizer_name.pop()
        fertilizer_dosage.pop()
        for index, element in enumerate(fertilizer_name):
            cursor.execute(
                f"SELECT CO2e FROM fertilizer WHERE name = '{translate[element]}'")
            data = cursor.fetchall()
            fertilizer_insert += f"{translate[element]}, "
            total_co2e += data[0][0] * \
                float(fertilizer_dosage[index]) * 0.001
        logger.info(total_co2e)  # total_co2e
        logger.info(fertilizer_insert)
        insertQuery = """INSERT INTO product VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        cursor.execute(insertQuery,
                       (information[3], information[0], information[1], information[2],
                        fertilizer_insert, fertilizer_integrate[1].replace(
                           '//', ', '), "None", '0',
                        total_co2e, 0.0, total_co2e, currentDateTime))

        connection.commit()
        close_connect(connection, cursor)
        return None
    except Exception as e:
        return e
