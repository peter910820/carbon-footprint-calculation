import psycopg2

DATABASE_URL = 'postgres://university_topic_user:QTv1CNqIdUAliShL1DldMYWaqV9wnhc0@dpg-cfvpfqt269v0ptn4thtg-a.oregon-postgres.render.com/university_topic'

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE product_information (
    grow_crops VARCHAR(199) NOT NULL,
    area VARCHAR(199) NOT NULL,
    Fertilizer VARCHAR(199),
    dosage DOUBLE PRECISION,
    Fertilizer_co2e DOUBLE PRECISION,
    co2_co2e DOUBLE PRECISION,
    methane_co2e DOUBLE PRECISION,
    final_co2e DOUBLE PRECISION NOT NULL);''')

cursor.execute('''CREATE TABLE fertilizer (
    name VARCHAR(199) NOT NULL,
    unit VARCHAR(199),
    N_kg DOUBLE PRECISION,
    P2O5_kg DOUBLE PRECISION,
    K2O_kg DOUBLE PRECISION);''')

cursor.execute('''CREATE TABLE sensor_data (
    ppm DOUBLE PRECISION NULL,
    time TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP);''')

cursor.execute('''create table fertilizer_use (
    type VARCHAR(199),
    dosage DOUBLE PRECISION,
    time TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP);''')



conn.commit()
print('suc')

cursor.close()
conn.close()