from fastapi import HTTPException
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from models.requestmodels import TextInput

model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

async def analyzesentiment(input_data: TextInput):
    result = classifier(input_data.text)
    if not result:
        raise HTTPException(status_code=500, detail="Sentiment analysis failed.")
    
    sentiment = result[0]
    emoji = "😊" if sentiment['label'] == "POSITIVE" else "😢"
    
    return {
        "label": sentiment['label'],
        "score": str(sentiment['score']),  # Convert score to string
        "emoji": emoji
    }