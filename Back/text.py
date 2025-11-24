from textblob import TextBlob
from textblob.en import sentiment

from Back.db import Journal
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# Receives users message, save message to db, analyze the message with TextBlob
# save message score to db, return mode based on message score
async def classify_message(message, session: AsyncSession):
    try:
        testimonial = TextBlob(message)
        mode_score = testimonial.sentiment.polarity

        mode: str
        if mode_score <= -0.5:
          mode = "Very Negative"
        elif mode_score < 0:
          mode = "Negative"
        elif mode_score == 0:
          mode = "Neutral"
        elif mode_score < 0.5:
          mode = "Positive"
        else:
          mode = "Very Positive"

        # Save to db
        journal = Journal(
          message=message,
          sentiment_score=mode_score,
          mode=mode
        )
        session.add(journal)
        await session.commit()
        await session.refresh(journal)

        return mode, mode_score

    except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))





