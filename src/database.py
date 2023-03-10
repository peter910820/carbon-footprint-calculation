import psycopg2

DATABASE_URL = 'postgres://university_topic_user:QTv1CNqIdUAliShL1DldMYWaqV9wnhc0@dpg-cfvpfqt269v0ptn4thtg-a.oregon-postgres.render.com/university_topic'

def show_product_information():
    database = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = database.cursor()   
    print('DB Words is connect ok!')
    cursor.execute("SELECT * FROM product_information")
    rows = cursor.fetchall()
    t0,t1,t2,t3,t4,t5,t6,t7 = [],[],[],[],[],[],[],[]
    db0 = []
    for row in rows:
        t0.append(row[0])
        t1.append(row[1])
        t2.append(row[2])
        t3.append(row[3])
        t4.append(row[4])
        t5.append(row[5])
        t6.append(row[6])
        t7.append(row[7])
    for column in range(len(t0)):
        n = [t0[column],t1[column],t2[column],t3[column],t4[column],t5[column],t6[column],t7[column]]
        db0.append(n)
    return db0

def show_fertilizer():
    database = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = database.cursor()   
    print('DB Words is connect ok!')
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

def show_sensor_data():
    database = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = database.cursor()   
    print('DB Words is connect ok!')
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

def show_fertilizer_use():
    database = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = database.cursor()   
    print('DB Words is connect ok!')
    cursor.execute("SELECT * FROM fertilizer_use")
    rows = cursor.fetchall()
    t0,t1,t2= [],[],[]
    db0 = []
    for row in rows:
        t0.append(row[0])
        t1.append(row[1])
        t2.append(row[2])
    for column in range(len(t0)):
        n = [t0[column],t1[column],t2[column]]
        db0.append(n)
    return db0