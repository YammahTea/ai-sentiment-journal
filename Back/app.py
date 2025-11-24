from fastapi import FastAPI, HTTPException
from Back.text import classify_message

app = FastAPI()

@app.get("/messages")
def messages() -> dict[str, bool | str]:
  return {"Retrieve": True, "Message": "some messages"}

@app.post("/journal")
def analyze_message(text:str) -> str:
  # mode = classify_message(text)
  mode = "positive"
  return mode


