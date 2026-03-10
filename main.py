<!DOCTYPE html>
<html>
<head>import os
import uvicorn
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sheets import search_sheets

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Homepage GET
@app.get("/")
def read_index():
    return FileResponse("static/index.html")

# Homepage HEAD for health checks
@app.head("/")
def head_index():
    return FileResponse("static/index.html")

# API endpoint for searching the spreadsheet
@app.get("/api/find")
async def find(number: str = Query(...), threshold: int = Query(1)):
    """
    number: string to search
    threshold: max Levenshtein distance for fuzzy matching (default=1)
    """
    return await search_sheets(number, threshold)

# Run app with dynamic Render port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
<title>Sheet Search</title>

<style>
body{
font-family:Arial;
margin:40px;
}

table{
border-collapse:collapse;
}

td,th{
border:1px solid #ccc;
padding:8px;
}
</style>

</head>

<body>

<h2>Google Sheet Search</h2>

<form method="post">
<input name="search" placeholder="Enter code (703, 723F, etc)">
<button type="submit">Search</button>
</form>

<br>

<table>

{% for row in results %}

<tr>
{% for cell in row %}
<td>{{cell}}</td>
{% endfor %}
</tr>

{% endfor %}

</table>

</body>
</html>

