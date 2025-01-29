# Google Spreadsheets to PDF

Simple way to save Google Sheets to PDF.

Features:
- Work **without** Apps Script.
- Open a spreadsheet by **id**.
- Save every day with **schedule**.
- **Docker** containerd.
- **Download** by url.

## Environment

- **SPREADSHEET_ID** - Google Sheet ID from environment variable
- **OUTPUT_PATH Final** - merged PDF file path
- **INCLUDE_SHEETS** - Comma-separated GID list of specific pages to export (if empty, the entire file is exported)
- **SAVE_EVERY_DAY_AT** - Save the filet every minute:hour (if empty, run once!)

### Google Sheet ID

Copy this from **Your-Google-Sheet-ID**

https://docs.google.com/spreadsheets/d/Your-Google-Sheet-ID/edit


### Google Sheet Access
In the access settings, you must specify at **least** "Everyone who has the link" -> **Read**


## Python Usage
```bash
pip install -r requirements.txt 
python main.py 
```

## Docker Usage

```bash 
docker build -t daniilantonenko/gs2p .
docker run -d \
-v /path/to/your/host/directory:/app/files \
-e SPREADSHEET_ID='YourSpreadSheet-ID' \
--name save_sheets gs2p
```

### Get file by HTTP
```bash
curl --output output.pdf "http://your-host:8080/files/output.pdf"
```