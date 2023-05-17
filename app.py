import uvicorn, os, psycopg2, datetime
# from dotenv import load_dotenv
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
    name: str

@app.get("/", response_class=HTMLResponse)
async def product_information(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/maindata-insert", response_class=HTMLResponse)
async def maindata(request: Request, information: list = Form(...), 
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
        print(database.maindata_insert(information, fertilizer_integrate))
        return templates.TemplateResponse("success.html", {"request": request})
    except Exception as error:
        return templates.TemplateResponse("error.html", {"request": request, "error": error})  

@app.get("/show-table/{table}", response_class=HTMLResponse)
async def show_table(request: Request, table):
    database = DatabaseConnect()
    datas = database.select_table(table)
    if datas != 1:
        return templates.TemplateResponse("show_table.html", {"request": request, 'table' : table, 'datas' : datas})
    error = "ERROR: This table is not exist."
    return templates.TemplateResponse("error.html", {"request": request, "error": error})

@app.get("/insert/{table}", response_class=HTMLResponse)
async def insert_table(request: Request, table):
    match table:
        case "fertilizer":
            return templates.TemplateResponse("fertilizer.html", {"request": request})
        case "sensor_data":
            return templates.TemplateResponse("sensor_data.html", {"request": request})

@app.post("/submit/{table}", response_class=HTMLResponse)
async def submit_table(request: Request, table, information : list = Form(...)):
    try:
        database = DatabaseConnect()
        match table:
            case "fertilizer":
                print(database.fertilizer_insert(information))
            case "sensor":
                print(database.sensor_insert(information))
        return templates.TemplateResponse('success.html',{'request':request})
    except Exception as error:
        print(error)
        return templates.TemplateResponse('error.html',{'request': request,"error": error})

@app.post("/sd", response_class=HTMLResponse)
async def sensor_data(request: Request, data : Data):
    data_dict = data.dict()
    print(data_dict['name'])
    data_dict['name'] = data_dict['name'].replace('[','')
    data_dict['name'] = data_dict['name'].replace(']','')
    s = float(data_dict['name'][-1])
    conn = psycopg2.connect("postgres://university_topic_user:QTv1CNqIdUAliShL1DldMYWaqV9wnhc0@dpg-cfvpfqt269v0ptn4thtg-a.oregon-postgres.render.com/university_topic", sslmode='require')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO sensor_data (ppm) VALUES ({s})")
    conn.commit()

# if __name__ == "__main__":
#     port = int(os.environ.get('PORT', 5000))
#     uvicorn.run("app:app", host="127.0.0.1", port=port, reload=True)