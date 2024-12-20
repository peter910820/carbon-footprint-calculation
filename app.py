import os
import psycopg2
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

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
        return templates.TemplateResponse('error.html', {'request': request, "error": str(e)})
    return templates.TemplateResponse('success.html', {'request': request})


@app.post("/product", response_class=HTMLResponse)  # insert product data
async def insert_product(request: Request, information: list = Form(...),
                         information_fertilizer: list = Form(...),
                         information_dosage_fertilizer: list = Form(...)):
    e = product_insert_handler(
        information, information_fertilizer, information_dosage_fertilizer)

    if e is not None:
        return templates.TemplateResponse("error.html", {"request": request, 'error': str(e)})
    return templates.TemplateResponse("success.html", {"request": request})


# get product data
@app.post("/product/{username}", response_class=HTMLResponse)
async def product_get(request: Request, username: str):
    product_data, sensor_data, e = product_get_handler(username)
    if e is not None:
        return templates.TemplateResponse("error.html", {"request": request, "error": e})
    if product_data == None and sensor_data == None:
        return templates.TemplateResponse("error.html", {"request": request, "error": "couldn't find user"})
    if sensor_data == None:
        sensor_data = 1
    logger.success("get product data success")
    return templates.TemplateResponse("show_table.html", {"request": request, 'table': username, 'main_data': product_data, "sensor_data": sensor_data})


# fertilizer insert page
@app.get("/insert/fertilizer", response_class=HTMLResponse)
async def insert_fertilizer(request: Request):
    return templates.TemplateResponse("fertilizer.html", {"request": request})


@app.post("/sensor", response_class=HTMLResponse)  # sensor handler
async def sensor_data(request: Request, data: Data):
    e = sensor_handler(data)
    if e is not None:
        logger.warning(e)
        return Response(status_code=500)
    logger.success("sensor data is sending successful")
    return Response(status_code=200)

if __name__ == "__main__":
    load_dotenv()
    port = int(os.environ.get('PORT', os.getenv('APP_PORT')))
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=True)
