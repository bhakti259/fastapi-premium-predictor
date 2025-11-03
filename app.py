import pickle
from typing import Annotated, Literal
from fastapi import Body, FastAPI, Path, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field, field_validator
import pickle
import pandas as pd

# Load the pre-trained model
with open("model.pkl", "rb") as f:
    model_data = pickle.load(f)
    model = model_data["model"]  # Use the pipeline inside the dict
    model_columns = model_data["model_columns"]  # Optional if you need it


    
app = FastAPI(title="patients management system", version="1.0.0")

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

class UserInput(BaseModel):
    age: Annotated[int, Field(..., ge=0, le=120, description="Age of the patient")]
    weight: Annotated[float, Field(..., ge=0, le=500, description="Weight of the patient in kg")]
    height: Annotated[float, Field(..., ge=0, le=300, description="Height of the patient in cm")]
    smoker: Annotated[bool, Field(..., description="Whether the patient is a smoker")]
    income_lpa: Annotated[float, Field(..., ge=0, description="Income level of the patient in LPA")]
    occupation: Annotated[Literal['retired', 'employed', 'unemployed', 'freelancer', 'student', 'business_owner'], Field(..., description="Occupation of the patient")]
    city: Annotated[str, Field(..., description="City of residence of the patient")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        if self.height > 0:
            return self.weight / ((self.height / 100) ** 2)
        return 0.0
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
       if self.smoker and self.bmi > 30:
            return 'high'
       elif self.smoker or self.bmi > 30:
           return 'medium'
       return 'low'
   
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 18:
            return 'child'
        elif 18 <= self.age < 65:
            return 'adult'
        return 'senior'
    
    @computed_field
    @property
    def city_tier(self) -> str:
        if self.city in tier_1_cities:
            return 'tier_1'
        elif self.city in tier_2_cities:
            return 'tier_2'
        return 'tier_3'     
    
@app.post("/predict")
def predict_premium(data: UserInput):
    try:
        input_df =pd.DataFrame([{
            'bmi' : data.bmi,
            'lifestyle_risk' : data.lifestyle_risk,
            'age_group' : data.age_group,   
            'city_tier' : data.city_tier,
            'income_lpa' : data.income_lpa,
            'occupation' : data.occupation
        }])
        
        prediction = model.predict(input_df)[0]
        return JSONResponse(status_code=200, content={"predicted_premium": prediction})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))