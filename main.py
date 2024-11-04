from fastapi import FastAPI, Request, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from models.requestmodels import TextInput
from services.translateservice import translate
from services.analyzesentimentservice import analyzesentiment
from services.questionanswer import getanswer
from typing import Dict
import time

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/css", StaticFiles(directory="css"), name="css")

@app.get("/translate", response_class=HTMLResponse)
async def page_translate(request: Request):
    css_version = int(time.time())
    return templates.TemplateResponse("languagetranslation.html", {"request": request, "css_version": css_version})

@app.get("/analyze-sentiment", response_class=HTMLResponse)
async def page_analyzesentiment(request: Request):
    css_version = int(time.time())
    return templates.TemplateResponse("sentimentanalysis.html", {"request": request, "css_version": css_version})

@app.get("/answer", response_class=HTMLResponse)
async def page_getanswer(request: Request):
    css_version = int(time.time())
    return templates.TemplateResponse("questionanswer.html", {"request": request, "css_version": css_version})

@app.post("/translate")
async def api_translate(request: Request):
        return await translate(request)

@app.post("/analyze-sentiment", response_model=Dict[str, str])
async def api_analyzesentiment(input_data: TextInput):
    return await analyzesentiment(input_data)

@app.post("/answer")
async def api_getanswer(question: str = Form(...), file: UploadFile = File(...)):
    return await getanswer(question, file)