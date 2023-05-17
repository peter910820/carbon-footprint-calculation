import psycopg2, datetime

class DatabaseConnect:

    def __init__(self):
        self.remind_message = 'Database is connect OK!'
        self.DATABASE_URL = 'postgres://university_topic_user:QTv1CNqIdUAliShL1DldMYWaqV9wnhc0@dpg-cfvpfqt269v0ptn4thtg-a.oregon-postgres.render.com/university_topic'
    
    def maindata_insert(self, information, fertilizer_integrate):
        currentDateTime = datetime.datetime.now()
        translate = {"urea": "尿素", "superphosphate": "過磷酸鈣", "potassium_chloride": "氯化鉀", "calcium_ammonium_nitrate": "硝酸銨鈣(肥料用)"}
        total_co2e = 0.0
        try:
            fertilizer_name = fertilizer_integrate[0].split("//")
            fertilizer_dosage = fertilizer_integrate[1].split("//")
            fertilizer_name.pop()
            fertilizer_dosage.pop()
            database = psycopg2.connect(self.DATABASE_URL, sslmode='require')
            print(self.remind_message)
            cursor = database.cursor()
            for index, element in enumerate(fertilizer_name):
                cursor.execute(f"SELECT CO2e FROM fertilizer WHERE name = '{translate[element]}'")
                data = cursor.fetchall()
                total_co2e += data[0][0] * float(fertilizer_dosage[index])
            print(total_co2e) # total_co2e

            insertQuery = """INSERT INTO product_information VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            print(fertilizer_integrate[0])
            print(information)
            print(type(fertilizer_integrate[0]))
            cursor.execute(insertQuery, 
                            (information[3], information[0], information[1], information[2],
                            fertilizer_integrate[0].replace('//',', '), fertilizer_integrate[1].replace('//',', '), "None",'0',
                            total_co2e, 0.0, total_co2e, currentDateTime))
            database.commit()
            cursor.close()
            database.close()
            return 0
        except Exception as error:
            return error
        
    def fertilizer_insert(self, information):
        try:
            database = psycopg2.connect(self.DATABASE_URL, sslmode='require')
            currentDateTime = datetime.datetime.now()
            cursor = database.cursor() 
            print(self.remind_message)
            insertQuery = """INSERT INTO fertilizer VALUES (%s, %s, %s, %s, %s, %s, %s);"""
            cursor.execute(insertQuery, 
                            (information[0], "公斤", information[1],
                            information[2], information[3], information[4], currentDateTime))
            database.commit()
            return 0
        except Exception as error:
            return error

    def sensor_insert(self, information):
        try:
            database = psycopg2.connect(self.DATABASE_URL, sslmode='require')
            currentDateTime = datetime.datetime.now()
            cursor = database.cursor() 
            print(self.remind_message)
            insertQuery = """INSERT INTO sensor_data VALUES (%s, %s);"""
            cursor.execute(insertQuery, (float(information[0]), currentDateTime))
            database.commit()
            cursor.close()
            database.close()
            return 0
        except Exception as error:
            return error
        
    def select_table(self, table_name):
        database = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cursor = database.cursor() 
        print(self.remind_message)
        if table_name in ["product_information", "fertilizer", "sensor_data"]:
            cursor.execute(f"SELECT * FROM {table_name}")
            data = cursor.fetchall()
            cursor.close()
            database.close()
            return data
        else:
            cursor.close()
            database.close()
            return 1
