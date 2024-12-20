import os
import psycopg2
import uvicorn

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from src.database import DatabaseConnect
from src.routes import *

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class Data(BaseModel):
    username: str
    data: str


@app.get("/", response_class=HTMLResponse)  # home page
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})


@app.get("/fertilizer", response_class=HTMLResponse)  # get fertilizer data
async def get_fertilizer(request: Request):
    data, e = fertilizer_get_handler()
    if e is not None:
        logger.error(e)
        templates.TemplateResponse(
            "error.html", {"request": request, "error": e})
    return templates.TemplateResponse("show_table.html", {"request": request, 'table': "fertilizer", 'datas': data})


@app.post("/fertilizer", response_class=HTMLResponse)  # insert fertilizer data
async def insert_fertilizer(request: Request, information: list = Form(...)):
    e = fertilizer_insert_handler(information)
    if e is not None:
        logger.error(e)
        return templates.TemplateResponse('error.html', {'request': request, "error": str(500)})
    return templates.TemplateResponse('success.html', {'request': request})


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
            return templates.TemplateResponse("error.html", {"request": request, 'error': str(status)})
        return templates.TemplateResponse("success.html", {"request": request})
    except Exception as error:
        return templates.TemplateResponse("error.html", {"request": request, "error": error})


@app.get("/insert/fertilizer", response_class=HTMLResponse)
async def insert_page(request: Request):
    return templates.TemplateResponse("fertilizer.html", {"request": request})


@app.post("/show-data", response_class=HTMLResponse)
async def show_table(request: Request, user: str = Form(...)):
    database = DatabaseConnect()
    main_data, sensor_data = database.search(user)
    if main_data == 1 and sensor_data == 1:
        return templates.TemplateResponse("error.html", {"request": request, "error": "couldn't find user"})
    return templates.TemplateResponse("show_table.html", {"request": request, 'table': user, 'main_data': main_data, "sensor_data": sensor_data})


@app.post("/sd", response_class=HTMLResponse)
async def sensor_data(request: Request, data: Data):
    DATABASE_URL = "postgres://seaotterms:T8Rh329KJna20gXJEtfYCLRhcb89BpE8@dpg-chrdh4bhp8ud4n4meprg-a.oregon-postgres.render.com/university_topic_xy0s"
    data_dict = data.dict()
    data = data_dict['data']
    name = data_dict['username']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO sensor_data (username, co2e) VALUES ('{name}', {data})")
    conn.commit()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=True)
