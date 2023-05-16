import uvicorn, os, psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form, Response, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from src.database import DatabaseConnect

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

load_dotenv()
DATABASE_URL =  os.getenv('DATABASE_URL')

class Data(BaseModel):
    name: str

@app.get("/", response_class=HTMLResponse)
async def product_information(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/show_table", response_class=HTMLResponse)
async def show_table(request: Request, table: str = Form(...)):
    database = DatabaseConnect()
    if table == '產品表格':
        data = database.show_product_information()
        table = 'product_information'
    elif table == '農藥表格':
        data = database.show_fertilizer()
        table = 'fertilizer'
    else:
        data = database.show_sensor_data()
        table = 'sensor_data'
    return templates.TemplateResponse("show_table.html", {"request": request, 'table' : table, 'data' : data})


@app.get("/product_information", response_class=HTMLResponse)
async def product_information(request: Request):
    return templates.TemplateResponse("product_information.html", {"request": request})

@app.get("/fertilizer", response_class=HTMLResponse)
async def fertilizer(request: Request):
    return templates.TemplateResponse("fertilizer.html", {"request": request})

@app.get("/sensor_data", response_class=HTMLResponse)
async def sensor_data(request: Request):
    return templates.TemplateResponse("sensor_data.html", {"request": request})

@app.post("/pi_insert", response_class=HTMLResponse)
async def pi_insert(request: Request, information : list = Form(...)):
    insert = []
    try:
        a = 0
        for i in information:
            if a == 0 or a == 2:
                insert.append(i)
            else:
                insert.append(float(i))
            a += 1
    except:
        print('輸入格式有誤')
        return
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO product_information VALUES (%s,%s,%s,%s,%s,%s)", (insert[0],insert[1],insert[2],insert[3],insert[4],insert[5]))
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

@app.post("/sd", response_class=HTMLResponse)
async def sensor_data(request: Request, data : Data):
    data_dict = data.dict()
    print(data_dict['name'])
    data_dict['name'] = data_dict['name'].replace('[','')
    data_dict['name'] = data_dict['name'].replace(']','')
    s = float(data_dict['name'][-1])
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO sensor_data (ppm) VALUES ({s})")
    conn.commit()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=True)