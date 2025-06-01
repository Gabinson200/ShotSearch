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

# Mount static files
app.mount("/", StaticFiles(directory="build", html=True), name="static")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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

@app.get("/")
def read_root():
    return {"message": "Welcome to Travel Vaccination Guide API"}

@app.post("/vaccination-info")
def get_vaccination_info(user_input: UserInput):
    try:
        # Simulated response - in production, this would fetch real data
        # For now, returning a sample response
        info = get_vaccination_info(rag_chain, user_input.specific_questions[0])
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
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
