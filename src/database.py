import psycopg2, datetime
import matplotlib.pyplot as plt

class DatabaseConnect:

    def __init__(self):
        self.DATABASE_URL = 'postgres://seaotterms:T8Rh329KJna20gXJEtfYCLRhcb89BpE8@dpg-chrdh4bhp8ud4n4meprg-a.oregon-postgres.render.com/university_topic_xy0s'
        self.translate = {"urea": "尿素", 
                          "superphosphate": "過磷酸鈣", 
                          "potassium_chloride": "氯化鉀", 
                          "calcium_ammonium_nitrate": "硝酸銨鈣(肥料用)"}
    
    def maindata_insert(self, information, fertilizer_integrate):
        currentDateTime = datetime.datetime.now()
        fertilizer_insert, total_co2e = "", 0.0
        try:
            fertilizer_name = fertilizer_integrate[0].split("//")
            fertilizer_dosage = fertilizer_integrate[1].split("//")
            fertilizer_name.pop()
            fertilizer_dosage.pop()
            database = psycopg2.connect(self.DATABASE_URL, sslmode='require')
            cursor = database.cursor()
            for index, element in enumerate(fertilizer_name):
                cursor.execute(f"SELECT CO2e FROM fertilizer WHERE name = '{self.translate[element]}'")
                data = cursor.fetchall()
                fertilizer_insert += f"{self.translate[element]}, "
                total_co2e += data[0][0] * float(fertilizer_dosage[index]) * 0.001
            print(total_co2e) # total_co2e
            print(fertilizer_insert)
            insertQuery = """INSERT INTO product_information VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
            cursor.execute(insertQuery, 
                            (information[3], information[0], information[1], information[2],
                            fertilizer_insert, fertilizer_integrate[1].replace('//',', '), "None",'0',
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
            insertQuery = """INSERT INTO fertilizer VALUES (%s, %s, %s, %s, %s, %s, %s);"""
            cursor.execute(insertQuery, 
                            (information[0], "公斤", information[1],
                            information[2], information[3], information[4], currentDateTime))
            database.commit()
            return 0
        except Exception as error:
            return error

    def fertilizer_show(self):
        database = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cursor = database.cursor()
        cursor.execute("SELECT * FROM fertilizer")
        data = cursor.fetchall()
        cursor.close()
        database.close()
        return data
    
    def search(self, user):
        database = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cursor = database.cursor()
        cursor.execute(f"SELECT * FROM product_information WHERE creater = '{user}'")
        main_data = cursor.fetchall()
        cursor.execute(f"SELECT * FROM sensor_data WHERE username = '{user}'")
        sensor_data = cursor.fetchall()
        if main_data == [] and sensor_data == []:
            cursor.close()
            database.close()
            return 1, 1
        if sensor_data == []:
            return main_data, 1
        else:
            data = [_[1] for _ in sensor_data]
            time = [_[2] for _ in sensor_data]
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
            print(data)
            print(time)
            plt.savefig("./static/chart.png")
        if main_data == []:
            cursor.close()
            database.close()
            return 1, sensor_data
        cursor.close()
        database.close()
        return main_data, sensor_data