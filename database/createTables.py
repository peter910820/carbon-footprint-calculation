import psycopg2, os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL =  os.getenv('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE product_information (
    creater VARCHAR(20) NOT NULL,
    grow_crops VARCHAR(20) NOT NULL,
    origin_place VARCHAR(20) NOT NULL,
    area DOUBLE PRECISION NOT NULL,
    fertilizer VARCHAR(100) NOT NULL,
    dosage_fertilizer DOUBLE PRECISION NOT NULL,
    pesticide VARCHAR(100) NOT NULL,
    dosage_pesticide DOUBLE PRECISION NOT NULL,
    fertilizer_co2e DOUBLE PRECISION NOT NULL,
    pesticide_co2e DOUBLE PRECISION NOT NULL,
    final_co2e DOUBLE PRECISION NOT NULL,
    time TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP);''')

cursor.execute('''CREATE TABLE fertilizer (
    name VARCHAR(199) NOT NULL,
    unit VARCHAR(199),
    N_kg DOUBLE PRECISION,
    P2O5_kg DOUBLE PRECISION,
    K2O_kg DOUBLE PRECISION,
    CO2e DOUBLE PRECISION,
    time TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP);''')

cursor.execute('''CREATE TABLE sensor_data (
    ppm DOUBLE PRECISION NULL,
    time TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP);''')

conn.commit()
print('success')

cursor.close()
conn.close()