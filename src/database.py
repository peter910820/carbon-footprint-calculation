import psycopg2

class DatabaseConnect:

    def __init__(self):
        self.remind_message = 'Database is connect OK!'
        self.DATABASE_URL = 'postgres://university_topic_user:QTv1CNqIdUAliShL1DldMYWaqV9wnhc0@dpg-cfvpfqt269v0ptn4thtg-a.oregon-postgres.render.com/university_topic'
    
    def maindata_insert(self, information, fertilizer_integrate):
        try:
            database = psycopg2.connect(self.DATABASE_URL, sslmode='require')
            print(self.remind_message)
            cursor = database.cursor()
            co2e, pointer = [], 0
            for f in fertilizer_integrate:
                cursor.execute(f"SELECT * FROM fertilizer WHERE {f} =")
                # 公式 * fertilizer_integrate[pointer]
                pointer += 1

            insertQuery = """INSERT INTO product_information VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            
            # cursor.execute(insertQuery, 
            #             (information[-1], information[0], information[1], information[2],
            #             article_array[6], f'{article_array[4]},{article_array[5]}', article_array[3], article_array[7],
            #             currentDateTime))
            # db.commit() 
            return
        except:
            print("ERROR: database insert failed.")
            return
    
    def show_product_information(self):
        database = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cursor = database.cursor()   
        print(self.remind_message)
        cursor.execute("SELECT * FROM product_information")
        rows = cursor.fetchall()
        t0,t1,t2,t3,t4,t5 = [],[],[],[],[],[]
        db0 = []
        for row in rows:
            t0.append(row[0])
            t1.append(row[1])
            t2.append(row[2])
            t3.append(row[3])
            t4.append(row[4])
            t5.append(row[5])
        for column in range(len(t0)):
            n = [t0[column],t1[column],t2[column],t3[column],t4[column],t5[column]]
            db0.append(n)
        return db0

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