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
            print(error)
            return 1
    
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


    def show_product_information(self):
        database = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cursor = database.cursor()   
        print(self.remind_message)
        cursor.execute("SELECT creater FROM product_information")
        rows = cursor.fetchall()
        print(rows)
        database.commit()
        cursor.close()
        database.close()
        return

    def show_fertilizer(self):
        database = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cursor = database.cursor()   
        print(self.remind_message)
        cursor.execute("SELECT * FROM fertilizer")
        rows = cursor.fetchall()
        t0,t1,t2,t3,t4 = [],[],[],[],[]
        db0 = []
        for row in rows:
            t0.append(row[0])
            t1.append(row[1])
            t2.append(row[2])
            t3.append(row[3])
            t4.append(row[4])
        for column in range(len(t0)):
            n = [t0[column],t1[column],t2[column],t3[column],t4[column]]
            db0.append(n)
        return db0

    def show_sensor_data(self):
        database = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cursor = database.cursor()   
        print(self.remind_message)
        cursor.execute("SELECT * FROM sensor_data")
        rows = cursor.fetchall()
        t0,t1 = [],[]
        db0 = []
        for row in rows:
            t0.append(row[0])
            t1.append(row[1])
        for column in range(len(t0)):
            n = [t0[column],t1[column]]
            db0.append(n)
        return db0