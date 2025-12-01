import pandas as pd
import pdfplumber

def parse_excel(file):
    df = pd.read_excel(file)
    summary = {
        "rows": len(df),
        "columns": list(df.columns),
        "preview": df.head(10).to_dict(orient="records")
    }
    return summary

def parse_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return {"text": text[:2000]}  # Safe truncation
