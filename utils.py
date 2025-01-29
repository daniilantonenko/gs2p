import requests
import os
from PyPDF2 import PdfMerger

def export_google_sheet_to_pdf(spreadsheet_id, output_dir, include_sheets=None, exclude_sheets=None):
    """Export specific sheets from a Google Sheets document as individual PDFs, then merge them into one."""
    
    export_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export"
    
    params = {
        'format': 'pdf',
        'size': 'A4',
        'portrait': 'true',
        'fitw': 'true',
        'top_margin': '0.5',
        'bottom_margin': '0.5',
        'left_margin': '0.65',
        'right_margin': '0.65',
        'gridlines': 'false',
        'printnotes': 'false',
        'sheetnames': 'true'
    }
    
    output_files = []

    # TODO Add add get all pages 
    # TODO Add exclude from all pages
    
    if include_sheets:  # Export only specific sheets
        for sheet_gid in include_sheets:
            if exclude_sheets and sheet_gid in exclude_sheets:  # Skip excluded sheets
                continue
            params['gid'] = sheet_gid
            response = requests.get(export_url, params=params, stream=True)
            output_path_sheet = os.path.join(output_dir, f"sheet_{sheet_gid}.pdf")
            if response.status_code == 200:
                with open(output_path_sheet, "wb") as file:
                    for chunk in response.iter_content(chunk_size=4096):
                        file.write(chunk)
                output_files.append(output_path_sheet)
                print(f"Successfully exported sheet GID {sheet_gid} to {output_path_sheet}")
            else:
                print(f"Failed to export sheet GID {sheet_gid}: {response.status_code}, {response.text}")
    else:  # Export all sheets if no specific sheets are provided
        response = requests.get(export_url, params=params, stream=True)
        output_path = os.path.join(output_dir, "all_sheets.pdf")
        if response.status_code == 200:
            with open(output_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=4096):
                    file.write(chunk)
            output_files.append(output_path)
            print(f"Successfully exported Google Sheet to {output_path}")
        else:
            print(f"Failed to export Google Sheet: {response.status_code}, {response.text}")
    
    return output_files

def merge_pdfs(pdf_paths, output_path):
    """Merge multiple PDF files into a single PDF."""
    merger = PdfMerger()
    for pdf_path in pdf_paths:
        merger.append(pdf_path)
    merger.write(output_path)
    merger.close()
    print(f"Successfully merged PDFs into {output_path}")


def save(spreadsheet_id, output_dir, include_sheets, exclude_sheets, output_path):   
    output_files = export_google_sheet_to_pdf(spreadsheet_id, output_dir, include_sheets, exclude_sheets)
    if output_files:
        merge_pdfs(output_files, output_path)
    
    # Clean up individual files
    for file_path in output_files:
        if os.path.exists(file_path):
            os.remove(file_path)
