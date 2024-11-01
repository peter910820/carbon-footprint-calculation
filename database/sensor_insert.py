import datetime
import os
import psycopg2
import time
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL =  os.getenv('DATABASE_URL')
currentDateTime = datetime.datetime.now()

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

for i in range(1,6):
    cursor.execute(f"INSERT INTO sensor_data (username, co2e) VALUES ('TEST2', '{0.11*i}')")
    conn.commit()
    
    print('success')
    time.sleep(10)


cursor.close()
conn.close()