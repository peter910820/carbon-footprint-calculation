import datetime
import matplotlib.pyplot as plt

from dotenv import load_dotenv
from loguru import logger
from typing import List, Optional, Tuple

from database.connect import connect_database
from pydantic import BaseModel


class Data(BaseModel):
    username: str
    data: str


def close_connect(connection, cursor):
    if cursor:
        cursor.close()
        logger.info("Close cursor success")
    if connection:
        connection.close()
        logger.info("Close connection success")


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


def product_get_handler(username) -> Tuple[Optional[List], Optional[List], Optional[Exception]]:
    try:
        load_dotenv()
        connection = connect_database()
        cursor = connection.cursor()
        cursor.execute(
            f"SELECT * FROM product WHERE creater = '{username}'")
        product_data = cursor.fetchall()
        cursor.execute(
            f"SELECT * FROM sensor_data WHERE username = '{username}'")
        sensor_data = cursor.fetchall()

        if len(product_data) == 0 and len(sensor_data) == 0:
            close_connect(connection, cursor)
            return None, None, None
        if len(sensor_data) == 0:
            return product_data, None, None
        else:
            data = [s[1] for s in sensor_data]
            time = [s[2] for s in sensor_data]
            if len(data) > 5:
                data = data[len(data)-5:]
                time = time[len(time)-5:]
            time = [t.strftime("%H:%M:%S") for t in time]
            plt.clf()
            plt.style.use('seaborn')
            plt.plot(time, data)
            plt.title("co2e time chart")
            plt.xlabel("time")
            plt.ylabel("co2e")
            logger.info(data)
            logger.info(time)
            plt.savefig("./static/chart.png")
        if len(product_data) == 0:
            close_connect(connection, cursor)
            return None, sensor_data, None
        close_connect(connection, cursor)
        return product_data, sensor_data, None
    except Exception as e:
        return None, None, e


def sensor_handler(sensor_data) -> Optional[Exception]:
    try:
        load_dotenv()
        connection = connect_database()
        cursor = connection.cursor()

        data_dict = sensor_data.dict()
        data = data_dict['data']
        name = data_dict['username']

        cursor.execute(
            f"INSERT INTO sensor_data (username, co2e) VALUES ('{name}', {data})")
        connection.commit()
        close_connect(connection, cursor)
        return None
    except Exception as e:
        return e
