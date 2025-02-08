import pandas as pd
from fpdf import FPDF
import os

def export_to_pdf(data):
    """
    Export the scorecard as a PDF file.
    """
    df = pd.DataFrame(data)
    file_path = 'scorecard.pdf'
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for col in df.columns:
        pdf.cell(40, 10, str(col), border=1)
    pdf.ln()
    
    for i in range(len(df)):
        for col in df.columns:
            pdf.cell(40, 10, str(df[col][i]), border=1)
        pdf.ln()
    
    pdf.output(file_path)
    return file_path

def export_to_excel(data):
    """
    Export the scorecard as an Excel file.
    """
    df = pd.DataFrame(data)
    file_path = 'scorecard.xlsx'
    df.to_excel(file_path, index=False)
    return file_path

def export_to_csv(data):
    """
    Export the scorecard as a CSV file.
    """
    df = pd.DataFrame(data)
    file_path = 'scorecard.csv'
    df.to_csv(file_path, index=False)
    return file_path