from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Back.text import classify_message

app = FastAPI()

class JournalEntry(BaseModel):
  text:str

@app.get("/messages")
def messages() -> dict[str, bool | str]:
  return {"Retrieve": True, "Message": "some messages"}

@app.post("/journal")
def analyze_message(entry: JournalEntry):
  try:
    mode, score = classify_message(entry.text)
    return mode, score
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))

