from flask import Flask, request, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import threading
import time
import os
import json

app = Flask(__name__)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials from environment variable
creds_dict = json.loads(os.environ["GOOGLE_CREDS"])

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

sheet = client.open("YOUR_SHEET_NAME").sheet1

sheet_data = []
search_index = {}

# ------------------------
# LOAD + INDEX SHEET
# ------------------------

def load_sheet():

    global sheet_data
    global search_index

    rows = sheet.get_all_values()
    sheet_data = rows

    index = {}

    for row_num, row in enumerate(rows):

        for cell in row:

            value = cell.lower()

            if value not in index:
                index[value] = []

            index[value].append(row_num)

    search_index = index

    print("Sheet loaded and indexed")


# ------------------------
# AUTO REFRESH THREAD
# ------------------------

def refresh_loop():

    while True:
        load_sheet()
        time.sleep(300)  # refresh every 5 minutes


threading.Thread(target=refresh_loop, daemon=True).start()


# ------------------------
# SEARCH FUNCTION
# ------------------------

def search_sheet(query):

    query = query.lower()
    results = []

    for row in sheet_data:

        for cell in row:
            if query in cell.lower():
                results.append(row)
                break

    return results


# ------------------------
# ROUTES
# ------------------------

@app.route("/", methods=["GET", "POST"])
def index():

    results = []

    if request.method == "POST":
        query = request.form["search"]
        results = search_sheet(query)

    return render_template("index.html", results=results)


if __name__ == "__main__":
    load_sheet()
    app.run()
