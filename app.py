import datetime
import os
import psycopg2
import uvicorn

from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from src.database import DatabaseConnect

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# load_dotenv()
# DATABASE_URL =  os.getenv('DATABASE_URL')

class Data(BaseModel):
    username: str
    data: str

@app.get("/", response_class=HTMLResponse)
async def product_information(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/search", response_class=HTMLResponse)
async def search(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.post("/maindata-insert", response_class=HTMLResponse)
async def submit_maindata(request: Request, information: list = Form(...), 
                   information_fertilizer: list = Form(...), 
                   information_dosage_fertilizer: list = Form(...)):
    fertilizer, dosage_fertilizer = '', ''
    fertilizer_integrate = []
    try:
        database = DatabaseConnect()
        for f in information_fertilizer:
            fertilizer += f"{f}//"
        for d_f in information_dosage_fertilizer:
            dosage_fertilizer += f"{d_f}//"
        fertilizer_integrate.append(fertilizer)
        fertilizer_integrate.append(dosage_fertilizer)
        status = database.maindata_insert(information, fertilizer_integrate)
        if status != 0:
            return templates.TemplateResponse("error.html", {"request": request, 'error' : str(status)})
        return templates.TemplateResponse("success.html", {"request": request})
    except Exception as error:
        return templates.TemplateResponse("error.html", {"request": request, "error": error})
    
@app.get("/insert/fertilizer", response_class=HTMLResponse)
async def insert_page(request: Request):
    return templates.TemplateResponse("fertilizer.html", {"request": request})

@app.post("/submit/fertilizer", response_class=HTMLResponse)
async def submit_table(request: Request, information : list = Form(...)):
    try:
        database = DatabaseConnect()
        status = database.fertilizer_insert(information)
        if status != 0:
            return templates.TemplateResponse('error.html',{'request': request, "error": str(status)})
        return templates.TemplateResponse('success.html',{'request':request})
    except Exception as error:
        print(error)
        return templates.TemplateResponse('error.html',{'request': request,"error": error})        

@app.post("/show-data", response_class=HTMLResponse)
async def show_table(request: Request, user : str = Form(...)):
    database = DatabaseConnect()
    main_data, sensor_data = database.search(user)
    if main_data == 1 and sensor_data == 1:
        return templates.TemplateResponse("error.html", {"request": request, "error": "couldn't find user"})
    return templates.TemplateResponse("show_table.html", {"request": request, 'table' : user, 'main_data' : main_data, "sensor_data": sensor_data })

@app.get("/show-data/fertilizer", response_class=HTMLResponse)
async def show_table(request: Request):
    database = DatabaseConnect()
    datas = database.fertilizer_show()
    if datas != 1:
        return templates.TemplateResponse("show_table.html", {"request": request, 'table' : "fertilizer", 'datas' : datas})
    error = "ERROR: This table is not exist."
    return templates.TemplateResponse("error.html", {"request": request, "error": error})

@app.post("/sd", response_class=HTMLResponse)
async def sensor_data(request: Request, data : Data):
    DATABASE_URL = "postgres://seaotterms:T8Rh329KJna20gXJEtfYCLRhcb89BpE8@dpg-chrdh4bhp8ud4n4meprg-a.oregon-postgres.render.com/university_topic_xy0s"
    data_dict = data.dict()
    data = data_dict['data']
    name = data_dict['username']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO sensor_data (username, co2e) VALUES ('{name}', {data})")
    conn.commit()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=True)