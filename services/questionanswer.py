from fastapi import File, UploadFile, Form
import requests

API_TOKEN = "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"
headers = {"Authorization": f"Bearer {API_TOKEN}"}
API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"

async def getanswer(question: str = Form(...), file: UploadFile = File(...)):
    file_content = await file.read()
    context = file_content.decode("utf-8")
    
    payload = {
        "inputs": {
            "question": question,
            "context": context
        }
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        answer = response.json().get("answer")
        return {"question": question, "answer": answer}
    else:
        return {"error": "Failed to fetch answer from Hugging Face API", "details": response.text}