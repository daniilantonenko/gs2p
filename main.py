import os
import schedule
import time
import sys
import socketserver
import threading
import functools

from utils import save
from handlers import Handler


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

def saver():
    if save_schedule:
        save_job = functools.partial(save, spreadsheet_id, output_dir, include_sheets, exclude_sheets, output_path)
        schedule.every().day.at(save_schedule).do(save_job)
        print(f'Schedule jobs: {schedule.jobs}')
        run_schedule()
    else:
        print("Start save spreadsheet:", spreadsheet_id)
        save(spreadsheet_id, output_dir, include_sheets, exclude_sheets, output_path)

output_dir = "./files"  # Temporary directory for individual PDFs
port = 8080 # Server port

# Env
spreadsheet_id = os.getenv("SPREADSHEET_ID")  # Google Sheet ID from environment variable
output_path = os.getenv("OUTPUT_PATH", "./files/output.pdf")  # Final merged PDF file
include_sheets = os.getenv("INCLUDE_SHEETS")  # Comma-separated GID list of specific pages to export
exclude_sheets = os.getenv("EXCLUDE_SHEETS")  # Comma-separated GID list of pages to exclude

# TODO: save_schedule = os.getenv("SAVE_SCHEDULE")  
save_schedule = os.getenv("SAVE_EVERY_DAY_AT")

if spreadsheet_id == "" or spreadsheet_id is None:
    sys.exit("Spreadsheet_id is empty")

# Convert string of GIDs to a list of integers if provided
if include_sheets:
    include_sheets = [int(gid) for gid in include_sheets.split(",")]
    print("Include sheets:", len(include_sheets))
if exclude_sheets:
    exclude_sheets = [int(gid) for gid in exclude_sheets.split(",")]
    print("Exclude sheets:", len(exclude_sheets))

# Run save in other thread
save_thread = threading.Thread(target=saver)
save_thread.start()    

with socketserver.TCPServer(("", port), Handler) as httpd:
    print(f"Server start at http://localhost:{port}/")
    httpd.serve_forever()