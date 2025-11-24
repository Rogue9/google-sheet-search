from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SPREADSHEET_ID = "1J_ZQkVy22gq_xDpD5K2enfY7pIKpjlpJAx9jeSzmqHA"

creds = Credentials.from_service_account_file(
    "serviceAccount.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
)

async def search_sheets(search_number: str):
    service = build("sheets", "v4", credentials=creds)

    metadata = service.spreadsheets().get(
        spreadsheetId=SPREADSHEET_ID
    ).execute()

    sheet_list = metadata.get("sheets", [])
    results = []

    for sheet in sheet_list:
        title = sheet["properties"]["title"]
        range_ = f"{title}!A:Z"

        data = service.spreadsheets().values().get(
            spreadsheetId=SPREADSHEET_ID,
            range=range_
        ).execute()

        rows = data.get("values", [])

        for row in rows:
            if any(search_number in str(cell) for cell in row):
                results.append({"sheet": title, "row": row})

    return results
