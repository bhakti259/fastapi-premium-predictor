## FastAPI Premium Predictor

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.111-green)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

## Overview
FastAPI Premium Predictor is a FastAPI-based application that predicts **insurance premium categories** (`Low`, `Medium`, `High`) based on user inputs. It uses a pre-trained machine learning model to provide predictions in real-time.

## Features
- Predict insurance premium category based on:
  - Age
  - Weight
  - Height
  - Smoking status
  - Income
  - Occupation
  - City tier
- Returns premium category as `Low`, `Medium`, or `High`
- Built with FastAPI for fast and interactive APIs
- Includes a trained ML model saved as `model.pkl`

## Installation

1. Clone the repository:
  ```bash
  git clone https://github.com/bhakti259/fastapi-premium-predictor.git
  Navigate to the project directory:

  bash
  Copy code
  cd fastapi-premium-predictor
  Create a virtual environment:

  bash
  Copy code
  python -m venv venv
  Activate the virtual environment:

  bash
  Copy code
  # Windows
  venv\Scripts\activate

  # macOS/Linux
  source venv/bin/activate
  Install dependencies:

  bash
  Copy code
  pip install -r requirements.txt

## Usage
Start the FastAPI server:

  bash
  Copy code
  uvicorn app:app --reload
  Open your browser and go to http://127.0.0.1:8000/docs to access the interactive API documentation.

## API Endpoint
  POST /predict
  Request Body (JSON):

    json
    {
      "age": 30,
      "weight": 60,
      "height": 1.7,
      "smoker": false,
      "income_lpa": 20,
      "occupation": "retired",
      "city": "Kolhapur"
    }
  Response Body (JSON):

    json
    {
      "predicted_premium": "Medium"
    }

## ML Model
  The ML model is saved as model.pkl.

  It uses features: bmi, age_group, lifestyle_risk, city_tier, income_lpa, and occupation.

  Preprocessing and encoding are included in the model pipeline, so no additional data transformation is needed before making predictions.

## License
This project is licensed under the MIT License.







