from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils import parse_excel, parse_pdf

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/file")
async def upload_file(file: UploadFile = File(...)):
    name = file.filename.lower()

    if name.endswith(".xlsx") or name.endswith(".xls"):
        result = parse_excel(file.file)
        return {"status": "success", "type": "excel", "result": result}

    elif name.endswith(".pdf"):
        result = parse_pdf(file.file)
        return {"status": "success", "type": "pdf", "result": result}

    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")
