import psycopg2, os, datetime
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL =  os.getenv('DATABASE_URL')
currentDateTime = datetime.datetime.now()

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

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
conn.commit()
print('success')

cursor.close()
conn.close()