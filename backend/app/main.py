from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from . import auth, analysis
from typing import Dict
import uvicorn

app = FastAPI(title="Finstop API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Lock this down in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
def register(user: auth.UserCreate):
    created = auth.create_user(user)
    if not created:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"status": "ok"}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    token = auth.authenticate_user_for_token(form_data.username, form_data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return token

@app.post("/upload")
async def upload_statement(file: UploadFile = File(...), current_user: auth.User = Depends(auth.get_current_user)):
    # Accept xlsx / csv / pdf
    content = await file.read()
    # Delegate to analysis parser
    try:
        parsed = analysis.parse_file(content, filename=file.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    ratios = analysis.compute_ratios(parsed)
    narrative = analysis.generate_expert_report(parsed, ratios, user_profile=current_user.username)
    return {"parsed": parsed, "ratios": ratios, "report": narrative}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
