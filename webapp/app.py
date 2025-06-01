from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import requests
import json
from backend import initialize_rag_chain, get_vaccination_info

app = FastAPI()
rag_chain = initialize_rag_chain()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    destination_country: str
    age: int
    vaccination_history: List[str]
    specific_questions: List[str]
    travel_date: str

#@app.get("/")
#def read_root():
#    return {"message": "Welcome to Travel Vaccination Guide API"}

@app.post("/vaccination-info")
def get_vaccination_info(user_input: UserInput):
    try:
        if not user_input.specific_questions:
            raise ValueError("No specific questions provided")
            
        # Get vaccination info from RAG chain
        info = get_vaccination_info(rag_chain, user_input.specific_questions[0])
        if info is None:
            raise ValueError("Failed to get response from RAG chain. Check if OpenAI API key is set and my_document.txt exists.")
            
        response = {
            "country": user_input.destination_country,
            "required_vaccinations": [
                info
            ],
            "recommended_vaccinations": [
                "Influenza" if user_input.age > 65 else None,
                "Hepatitis B" if user_input.age < 18 else None
            ],
            "specific_advice": [
                f"Based on your travel date ({user_input.travel_date}), make sure to get any required vaccinations at least 2 weeks before departure."
            ],
            "additional_notes": [
                "Check with your healthcare provider for personalized recommendations",
                "Travel insurance is recommended for medical emergencies"
            ]
        }
        
        # Filter out None values
        response["required_vaccinations"] = [v for v in response["required_vaccinations"] if v]
        response["recommended_vaccinations"] = [v for v in response["recommended_vaccinations"] if v]
        
        return response
    except Exception as e:
        import traceback
        error_details = f"Error: {str(e)}\nTraceback: {traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_details)

# Mount static files after API routes
app.mount("/", StaticFiles(directory="build", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
