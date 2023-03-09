import uvicorn, os, psycopg2
from fastapi import FastAPI, Request, Form, Response, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from src.database import *

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DATABASE_URL = 'postgres://university_topic_user:QTv1CNqIdUAliShL1DldMYWaqV9wnhc0@dpg-cfvpfqt269v0ptn4thtg-a.oregon-postgres.render.com/university_topic'

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    product_information = show_product_information()
    fertilizer = show_fertilizer()
    sensor_data = show_sensor_data()
    fertilizer_us = show_fertilizer_use()
    return templates.TemplateResponse("home.html", {"request": request, 'product_information' : product_information, 'fertilizer' : fertilizer, 'sensor_data' : sensor_data, 'fertilizer_us' : fertilizer_us})

@app.get("/product_information", response_class=HTMLResponse)
async def product_information(request: Request):
    return templates.TemplateResponse("product_information.html", {"request": request})

@app.get("/fertilizer", response_class=HTMLResponse)
async def fertilizer(request: Request):
    return templates.TemplateResponse("fertilizer.html", {"request": request})

@app.get("/sensor_data", response_class=HTMLResponse)
async def sensor_data(request: Request):
    return templates.TemplateResponse("sensor_data.html", {"request": request})

@app.get("/fertilizer_use", response_class=HTMLResponse)
async def sensor_data(request: Request):
    return templates.TemplateResponse("fertilizer_use.html", {"request": request})

@app.post("/pi_insert", response_class=HTMLResponse)
async def pi_insert(request: Request, information : list = Form(...)):
    insert = []
    try:
        a = 0
        for i in information:
            if a <= 2:
                insert.append(i)
            else:
                insert.append(float(i))
            a += 1
    except:
        print('輸入格式有誤')
        return
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO product_information VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (insert[0],insert[1],insert[2],insert[3],insert[4],insert[5],insert[6],insert[7]))
    conn.commit()
    print(insert)
    return templates.TemplateResponse('success.html',{'request':request})

@app.post("/fertilizer_insert", response_class=HTMLResponse)
async def fertilizer_insert(request: Request, information : list = Form(...)):
    insert = []
    try:
        a = 0
        for i in information:
            if a <= 1:
                insert.append(i)
            else:
                insert.append(float(i))
            a += 1
    except:
        print('輸入格式有誤')
        return
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO fertilizer VALUES (%s,%s,%s,%s,%s)", (insert[0],insert[1],insert[2],insert[3],insert[4]))
    conn.commit()
    print(insert)
    return templates.TemplateResponse('success.html',{'request':request})

@app.post("/sd_insert", response_class=HTMLResponse)
async def sd_insert(request: Request, ppm : str = Form(...)):
    try:
        ppm = float(ppm)
    except:
        print('輸入格式有誤')
        return
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO sensor_data (ppm) VALUES ({ppm})")
    conn.commit()
    print(ppm)
    return templates.TemplateResponse('success.html',{'request':request})

@app.post("/fu_insert", response_class=HTMLResponse)
async def fu_insert(request: Request, information : list = Form(...)):
    insert = []
    try:
        a = 0
        for i in information:
            if a == 0:
                insert.append(i)
            else:
                insert.append(float(i))
            a += 1
    except:
        print('輸入格式有誤')
        return
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO fertilizer_use (type,dosage) VALUES (%s,%s)", (insert[0],insert[1]))
    conn.commit()
    print(insert)
    return templates.TemplateResponse('success.html',{'request':request})



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)