import uvicorn,os
from fastapi import FastAPI, Request, HTTPException, Form, Cookie, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)