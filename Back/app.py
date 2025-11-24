from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from Back.text import classify_message
from Back.db import Journal, create_db_and_tables, get_async_session

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

class JournalEntry(BaseModel):
    text:str

@app.get("/messages")
async def messages(session: AsyncSession = Depends(get_async_session)):
    query = (select(Journal).order_by(Journal.created_at))

    result = await session.execute(query)
    journals = result.scalars().all()

    journal_data = []
    for journal in journals:
      journal_data.append({

        "id": str(journal.id),
        "message": journal.message,
        "sentiment_Score": journal.sentiment_score,
        "mode": journal.mode,
        "created_at": journal.created_at

      })
    return {"Journals": journal_data}

@app.post("/journal")
async def analyze_message(entry: JournalEntry, session: AsyncSession = Depends(get_async_session)):
    try:
      mode, score = await classify_message(entry.text, session)
      return mode, score
    except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))

