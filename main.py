import os
import uvicorn
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sheets import search_sheets

app = FastAPI()

# Mount static folder for index.html and other assets
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the homepage
@app.get("/")
def read_index():
    return FileResponse("static/index.html")

# API endpoint to search the spreadsheet
@app.get("/api/find")
async def find(query: str = Query(...)):
    return await search_sheets(number)

# Run using dynamic port (Render sets PORT environment variable)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

