"""
main.py - FastAPI-based Patient Management System

This module provides a FastAPI to manage patient records stored in a JSON file.
It supports operations such as creating, viewing, editing, sorting, and deleting
patient data. Each patient’s BMI and health verdict are automatically calculated
using Pydantic’s computed fields.

Author: Bhakti Kulkarni
Date: 2025-10-26
Version: 1.0.0
"""

from fastapi import Body, FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import List, Annotated, Literal, Optional
import json

# ---------------------------------------------------------------------------
# Initialize FastAPI Application
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Patients Management System API",
    version="1.0.0",
    description="A FastAPI-based system for managing patient records, "
                "including BMI calculation and health verdicts."
)

# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

class Patient(BaseModel):
    """
    Represents a patient record with personal and health details.

    Attributes:
        id (str): Unique identifier for the patient.
        name (str): Full name of the patient.
        city (str): City of residence.
        age (int): Age of the patient (must be between 1 and 119).
        gender (Literal): Gender of the patient ("Male", "Female", or "Other").
        height (float): Height in meters.
        weight (float): Weight in kilograms.
        bmi (float): Automatically computed Body Mass Index.
        verdict (str): Health verdict based on BMI.
    """
    id: Annotated[str, Field(..., description="Unique identifier for the patient", example="P001")]
    name: Annotated[str, Field(..., description="Full name of the patient", example="John Doe")]
    city: Annotated[str, Field(..., description="City of residence", example="New York")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient", example=30)]
    gender: Annotated[Literal["Male", "Female", "Other"], Field(..., description="Gender of the patient", example="Male")]
    height: Annotated[float, Field(..., gt=0, description="Height in meters", example=1.75)]
    weight: Annotated[float, Field(..., gt=0, description="Weight in kilograms", example=70.0)]

    @computed_field
    @property
    def bmi(self) -> float:
        """Compute and return the Body Mass Index (BMI)."""
        if self.height > 0:
            return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        """Return a health verdict based on the BMI value."""
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"


class PatientUpdate(BaseModel):
    """
    Represents partial updates to an existing patient record.
    All fields are optional to allow selective updating.
    """
    name: Annotated[Optional[str], Field(None, description="Full name of the patient", example="John Doe")]
    city: Annotated[Optional[str], Field(None, description="City of residence", example="New York")]
    age: Annotated[Optional[int], Field(None, gt=0, lt=120, description="Age of the patient", example=30)]
    gender: Annotated[Optional[Literal["Male", "Female", "Other"]], Field(None, description="Gender of the patient", example="Male")]
    height: Annotated[Optional[float], Field(None, gt=0, description="Height in meters", example=1.75)]
    weight: Annotated[Optional[float], Field(None, gt=0, description="Weight in kilograms", example=70.0)]


# ---------------------------------------------------------------------------
# Utility Functions
# ---------------------------------------------------------------------------

def loadData():
    """
    Load patient data from the 'patients.json' file.

    Returns:
        dict: Parsed JSON data containing patient records.

    Raises:
        FileNotFoundError: If the 'patients.json' file does not exist.
    """
    with open("patients.json", "r") as f:
        data = json.load(f)
    return data


def saveData(data: dict):
    """
    Save patient data to the 'patients.json' file.

    Args:
        data (dict): Dictionary containing all patient records to be saved.
    """
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------

@app.get("/")
def hello():
    """
    Root endpoint.

    Returns:
        dict: Welcome message for the Patients Management System API.
    """
    return {"message": "Patients Management System API"}


@app.get("/about")
def about():
    """
    Retrieve metadata about the API.

    Returns:
        dict: Application name, version, and description.
    """
    return {
        "app": "Patients Management System",
        "version": "1.0.0",
        "description": "API for managing patient records."
    }


@app.get("/view")
def view():
    """
    Retrieve all patient records.

    Returns:
        dict: Complete list of all patients stored in the database.
    """
    data = loadData()
    return data


@app.get("/patient/{patient_id}")
def get_patient(patient_id: str = Path(..., description="The ID of the patient to retrieve", example="P001")):
    """
    Retrieve details of a specific patient by ID.

    Args:
        patient_id (str): Unique ID of the patient.

    Returns:
        dict: Patient details if found.

    Raises:
        HTTPException: If the patient is not found.
    """
    data = loadData()
    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort patients by height, weight, or bmi", example="height"),
    order: str = Query("asc", description="Order of sorting: asc or desc", example="asc")
):
    """
    Sort patients by a specific attribute (height, weight, or BMI).

    Args:
        sort_by (str): Field to sort by.
        order (str): Sorting order ("asc" or "desc").

    Returns:
        list: Sorted list of patients.

    Raises:
        HTTPException: If sort field or order is invalid.
    """
    valid_fields_sort_by = ["height", "weight", "bmi"]
    if sort_by not in valid_fields_sort_by:
        raise HTTPException(status_code=400, detail=f"Invalid sort_by field. Must be one of {valid_fields_sort_by}")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Must be 'asc' or 'desc'")

    sort_order = False if order == "asc" else True
    data = loadData()
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)
    return sorted_data


@app.post("/create")
def create_patient(patient: Patient):
    """
    Create a new patient record.

    Args:
        patient (Patient): New patient details.

    Returns:
        JSONResponse: Success message if created successfully.

    Raises:
        HTTPException: If a patient with the same ID already exists.
    """
    data = loadData()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")

    data[patient.id] = patient.model_dump(exclude=["id"])
    saveData(data)

    return JSONResponse(content={"message": "Patient created successfully"}, status_code=201)


@app.put("/edit/{patient_id}")
def edit_patient(patient_id: str, patient_update: PatientUpdate):
    """
    Update an existing patient record by ID.

    Args:
        patient_id (str): ID of the patient to update.
        patient_update (PatientUpdate): Fields to be updated.

    Returns:
        JSONResponse: Success message after update.

    Raises:
        HTTPException: If the patient is not found.
    """
    data = loadData()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing_patient_data = data[patient_id]
    updated_data = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
        existing_patient_data[key] = value

    # Update computed fields (BMI & verdict)
    existing_patient_data["id"] = patient_id
    patient_obj = Patient(**existing_patient_data)
    existing_patient_data = patient_obj.model_dump(exclude=["id"])

    data[patient_id] = existing_patient_data
    saveData(data)

    return JSONResponse(content={"message": "Patient updated successfully"}, status_code=200)


@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    """
    Delete a patient record by ID.

    Args:
        patient_id (str): ID of the patient to delete.

    Returns:
        JSONResponse: Success message after deletion.

    Raises:
        HTTPException: If the patient is not found.
    """
    data = loadData()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    del data[patient_id]
    saveData(data)

    return JSONResponse(content={"message": "Patient deleted successfully"}, status_code=200)
