import datetime

from dotenv import load_dotenv
from loguru import logger

from connect import connect_database


def create_tables(cursor):
    cursor.execute(
        '''
        CREATE TABLE product_information (
        creater VARCHAR(20) NOT NULL,
        grow_crops VARCHAR(20) NOT NULL,
        origin_place VARCHAR(20) NOT NULL,
        area DOUBLE PRECISION NOT NULL,
        fertilizer VARCHAR(100) NOT NULL,
        dosage_fertilizer VARCHAR(100) NOT NULL,
        pesticide VARCHAR(100) NOT NULL,
        dosage_pesticide VARCHAR(100) NOT NULL,
        fertilizer_co2e DOUBLE PRECISION NOT NULL,
        pesticide_co2e DOUBLE PRECISION NOT NULL,
        final_co2e DOUBLE PRECISION NOT NULL,
        time TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP);
        ''')

    cursor.execute(
        '''
        CREATE TABLE fertilizer (
        name VARCHAR(199) NOT NULL,
        unit VARCHAR(199),
        N_kg DOUBLE PRECISION,
        P2O5_kg DOUBLE PRECISION,
        K2O_kg DOUBLE PRECISION,
        CO2e DOUBLE PRECISION,
        time TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP);
        ''')

    cursor.execute(
        '''
        CREATE TABLE sensor_data (
        username VARCHAR(30) NOT NULL,
        co2e DOUBLE PRECISION NOT NULL,
        time TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP);
        ''')


def fertilizer_insert(cursor):
    currentDateTime = datetime.datetime.now()
    insertQuery = """INSERT INTO fertilizer VALUES (%s, %s, %s, %s, %s, %s, %s);"""

    cursor.execute(insertQuery,
                   ('尿素', '公斤', 18.4,
                    0, 0, 1.65, currentDateTime))
    cursor.execute(insertQuery,
                   ('過磷酸鈣', '公斤', 0,
                    7.2, 0, 0.847, currentDateTime))
    cursor.execute(insertQuery,
                   ('氯化鉀', '公斤', 0,
                    0, 24, 0.61, currentDateTime))
    cursor.execute(insertQuery,
                   ('硝酸銨鈣(肥料用)', '公斤', 0,
                    0, 0, 1.8, currentDateTime))


def main():
    try:
        load_dotenv()
        connection = connect_database()
        if connection is None:
            return
        cursor = connection.cursor()

        create_tables(cursor)  # create tables
        connection.commit()
        logger.success("Create tables success")

        fertilizer_insert(cursor)  # insert basic fertilizer
        connection.commit()
        logger.success("Insert fertilizer data success")
    except Exception as e:
        if connection:
            connection.rollback()
        logger.error(e)
    finally:
        if cursor:
            cursor.close()
            logger.info("Close cursor success")
        if connection:
            connection.close()
            logger.info("Close connection success")


if __name__ == "__main__":
    main()
