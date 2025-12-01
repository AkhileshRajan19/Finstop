from typing import Dict, Any
import pandas as pd
import io
import pdfplumber
import numpy as np

def parse_excel(content: bytes) -> Dict[str, Any]:
    xls = pd.ExcelFile(io.BytesIO(content))
    out = {}
    for sheet in xls.sheet_names:
        df = xls.parse(sheet, header=0)
        df = df.replace({np.nan: None})
        out[sheet] = df.fillna("").to_dict(orient="list")
    return {"type": "excel", "sheets": out}

def parse_pdf(content: bytes) -> Dict[str, Any]:
    out_tables = []
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for t in tables:
                if len(t) >= 1:
                    df = pd.DataFrame(t[1:], columns=t[0])
                    out_tables.append(df.fillna("").to_dict(orient="list"))
    return {"type": "pdf", "tables": out_tables}

def parse_file(content: bytes, filename: str) -> Dict[str, Any]:
    lower = filename.lower()
    if lower.endswith(".xlsx") or lower.endswith(".xls") or lower.endswith(".csv"):
        return parse_excel(content)
    if lower.endswith(".pdf"):
        return parse_pdf(content)
    raise ValueError("Unsupported file type")

def compute_ratios(parsed: Dict[str, Any]) -> Dict[str, Any]:
    ratios = {}
    sheets = parsed.get("sheets") or {}
    def try_df(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                try:
                    df = pd.DataFrame(v)
                    return df
                except:
                    continue
        return None
    bs = try_df(sheets)
    if bs is not None:
        def find_value(df, candidates):
            for cand in candidates:
                matches = [c for c in df.columns if cand.lower() in c.lower()] + [c for c in df.index if cand.lower() in str(c).lower()]
                if matches:
                    col = matches[0]
                    try:
                        vals = pd.to_numeric(df[col].astype(str).str.replace(",",""), errors='coerce').dropna()
                        if len(vals) > 0:
                            return float(vals.iloc[-1])
                    except:
                        pass
            return None
        total_assets = find_value(bs, ["Total Assets", "Assets"])
        total_liab = find_value(bs, ["Total Liabilities", "Liabilities"])
        equity = find_value(bs, ["Equity", "Total Equity", "Shareholders' Equity"])
        if total_assets and total_liab:
            ratios["debt_to_assets"] = total_liab / total_assets
        if total_assets and equity:
            ratios["equity_to_assets"] = equity / total_assets
    ratios.setdefault("current_ratio", None)
    ratios.setdefault("quick_ratio", None)
    ratios.setdefault("gross_margin", None)
    ratios.setdefault("net_profit_margin", None)
    return ratios

def generate_expert_report(parsed: Dict[str, Any], ratios: Dict[str, Any], user_profile: str = "Analyst") -> str:
    narrative_lines = []
    narrative_lines.append(f"Expert Financial Analysis for user: {user_profile}")
    narrative_lines.append("Summary of computed ratios:")
    for k, v in ratios.items():
        narrative_lines.append(f"- {k}: {v if v is not None else 'insufficient data'}")
    narrative_lines.append("")
    narrative_lines.append("Observations:")
    dta = ratios.get("debt_to_assets")
    if dta is not None:
        if dta > 0.6:
            narrative_lines.append("The company appears highly leveraged (debt-to-assets > 60%). Consider risk mitigation and refinancing.")
        elif dta < 0.3:
            narrative_lines.append("The company has conservative leverage.")
        else:
            narrative_lines.append("Leverage is moderate.")
    else:
        narrative_lines.append("Debt-to-assets could not be computed from provided statements.")
    narrative_lines.append("")
    narrative_lines.append("Recommendations:")
    narrative_lines.append("- Validate input statement mapping (ensure balance sheet and income statement are identified).")
    narrative_lines.append("- Consider trend analysis (3-5 years) and peer benchmarking.")
    narrative = "\n".join(narrative_lines)
    return narrative
