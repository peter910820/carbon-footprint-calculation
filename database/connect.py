import os
import psycopg2

from dotenv import load_dotenv
from loguru import logger


def connect_database():
    try:
        load_dotenv()
        connection = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
        logger.info("Database connection successful")
        return connection
    except Exception as e:
        logger.error(f"Connect fail: {e}")
        return None


if __name__ == "__main__":
    connect_database()
