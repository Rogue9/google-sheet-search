import os
import uvicorn
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sheets import search_sheets

app = FastAPI()

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Homepage
@app.get("/")
def read_index():
    return FileResponse("static/index.html")

# API endpoint for searching the spreadsheet
@app.get("/api/find")
async def find(number: str = Query(...)):  # Use str to allow letters and numbers
    return await search_sheets(number)
