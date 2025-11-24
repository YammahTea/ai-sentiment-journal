from textblob import TextBlob

#Recives users message, save message to db, analyze the message with TextBlob
# save message score to db, return mode based on message score
def classify_message(message):
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

    """ ˅˅˅ TO DO ˅˅˅ """
    # save message to db
    # save mode_score to db
    # save final sentiment to db
    """ ^^^ TO DO ^^^ """

    return mode, mode_score




