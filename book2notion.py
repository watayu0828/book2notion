import bs4
import os
import re
import requests
import sys
from dotenv import load_dotenv
from tkinter.filedialog import askopenfilename

# .envファイルを読み込む
load_dotenv(verbose=True)
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# ファイル選択
filename = askopenfilename(
    title="ファイル選択", filetypes=[("HTML ファイル", "*.html")]
)

try:
    with open(filename, "r", encoding="utf-8") as f:
        contents = f.read()
except:
    sys.exit(1)

soup = bs4.BeautifulSoup(contents, "html.parser")

# Title
div = soup.find("div", class_="bookTitle")
book_title = div.text.strip()

# Authors
div = soup.find("div", class_="authors")
authors = div.text.strip()

headers = {
    "Accept": "application/json",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
    "Authorization": "Bearer " + os.environ["TOKEN"],
}


def get_payload(text, page_num):
    return {
        "parent": {"type": "database_id", "database_id": os.environ["DATABASE_ID"]},
        "properties": {
            "Highlight": {
                "title": [
                    {"text": {"content": text}},
                ]
            },
            "Page": {"number": int(page_num)},
            "BookTitle": {"select": {"name": book_title, "color": "default"}},
            "Author": {"select": {"name": authors, "color": "default"}},
        },
    }


# ハイライトを抽出してNotionにPOST
note_heading = soup.find_all("div", class_="noteHeading")
note_text = soup.find_all("div", class_="noteText")
for count, value in enumerate(note_heading):
    # Page
    match = re.search(r"\sページ(.+)\s·位置\d+", value.text)
    if match:
        page_number = match.group(1)

    fixed_note_text = note_text[count].text.strip()
    payload = get_payload(fixed_note_text, page_number)
    response = requests.post(
        "https://api.notion.com/v1/pages", json=payload, headers=headers
    )
    print(response.text)
