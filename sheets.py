from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import Levenshtein

# Google Sheet ID
SPREADSHEET_ID = "1J_ZQkVy22gq_xDpD5K2enfY7pIKpjlpJAx9jeSzmqHA"

# Load service account credentials from secret file
creds = Credentials.from_service_account_file(
    "serviceAccount.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
)

async def search_sheets(search_number: str, threshold: int = 1):
    """
    Fuzzy search all sheets for the input string.
    - Case-insensitive
    - Letters, numbers, mixed codes
    - Tolerates small differences (default threshold=1)
    """
    search_lower = search_number.lower()
    service = build("sheets", "v4", credentials=creds)

    metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
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
            for cell in row:
                cell_str = str(cell).lower()
                if Levenshtein.distance(search_lower, cell_str) <= threshold:
                    results.append({"sheet": title, "row": row})
                    break  # Avoid duplicates
    return results
