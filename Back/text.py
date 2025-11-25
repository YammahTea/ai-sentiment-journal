from textblob import TextBlob
from textblob.en import sentiment

from Back.db import Journal
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

# Receives users message, save message to db, analyze the message with TextBlob
# save message score to db, return mood based on message score
async def classify_message(message, session: AsyncSession):
    try:
        testimonial = TextBlob(message)
        mood_score = testimonial.sentiment.polarity

        mood: str
        if mood_score <= -0.5:
          mood = "Very Negative"
        elif mood_score < 0:
          mood = "Negative"
        elif mood_score == 0:
          mood = "Neutral"
        elif mood_score < 0.5:
          mood = "Positive"
        else:
          mood = "Very Positive"

        # Save to db
        journal = Journal(
          message=message,
          sentiment_score=mood_score,
          mood=mood
        )
        session.add(journal)
        await session.commit()
        await session.refresh(journal)

        return mood, mood_score

    except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))





