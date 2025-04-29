from fastapi import FastAPI, HTTPException
from transformers import pipeline, Pipeline
from models.requestmodels import TextRequest
from models.responsemodels import SummaryResponse

app = FastAPI()

try:
    summarizer: Pipeline = pipeline("summarization", model="facebook/bart-large-cnn")
except Exception as e:
    raise RuntimeError(f"Failed to load the summarization model: {e}")


@app.post("/summarize", response_model=SummaryResponse)
async def summarize_text(request: TextRequest):
    if len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Input text is empty.")
    if len(request.text) < 10:
        raise HTTPException(status_code=400, detail="Input text is too short to summarize.")

    try:
        summary = summarizer(
            request.text,
            max_length=request.max_length,
            min_length=request.min_length,
            do_sample=False
        )
        return SummaryResponse(summary=summary[0]['summary_text'])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {e}")

