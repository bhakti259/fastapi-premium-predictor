##Patients Management System API - Documentation

Overview
A FastAPI-based backend system for managing patient records stored in a JSON file. The API supports creating, viewing, editing, sorting, and deleting patient data. Each patient's BMI and health verdict are automatically calculated using Pydantic’s computed fields.

Features
•	Create, view, edit, and delete patient records.
•	Automatically compute BMI (Body Mass Index) using Pydantic’s computed fields.
•	Generate health verdicts (Underweight, Normal, Overweight, Obesity) automatically.
•	Sort patient data by height, weight, or BMI.
•	JSON file-based storage — no database required.

Tech Stack
• Python 3.10+
• FastAPI
• Uvicorn
• Pydantic

Setup Instructions
1. Clone the repository and navigate to the folder.
2. Create a virtual environment and activate it.
3. Install dependencies using 'pip install -r requirements.txt'.
4. Run the server using 'uvicorn main:app --reload'.

API Endpoints
Method	Endpoint	Description
GET	/	Root welcome message
GET	/view	Retrieve all patients
GET	/patient/{patient_id}	Get details of a specific patient
POST	/create	Add a new patient
PUT	/edit/{patient_id}	Edit an existing patient
DELETE	/delete/{patient_id}	Remove a patient record
GET	/sort?sort_by=bmi&order=desc	Sort patients by BMI or other fields


Author
Bhakti Kulkarni
Version: 1.0.0
Date: 2025-10-26
