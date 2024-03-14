from fastapi import APIRouter, HTTPException
from app.utils.g_drive_service import GoogleDriveService

import joblib
import os

router = APIRouter()

# Define the directory for temporary data storage
TMP_DATA_DIR = "/tmp/data"

def load_model(model_id: str):
    model_path = os.path.join("data", model_id, "model.joblib")
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail=f"Model not found for model_id: {model_id}")
    return joblib.load(model_path)

@router.post('/predict/{model_id}')
async def predict(model_id: str, features: dict):
    # Load the model
    model = load_model(model_id)
    
    # Make prediction
    try:
        # Convert features to a 2-dimensional matrix
        feature_values = list(features.values())  # Extract feature values
        input_matrix = [feature_values]  # Reshape into a 2D array
        prediction = model.predict(input_matrix)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")

    return {"model_id": model_id, "predictions": prediction.tolist()}

#######################################################################################################################

# Function to load model
def load_model_from_file(model_id: str):
    model_path = os.path.join(TMP_DATA_DIR, model_id, "model.joblib")
    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail=f"Model not found for model_id: {model_id}")
    return joblib.load(model_path)

# Function to download model folder from Google Drive
def download_model_folder_from_drive(model_id: str):
    # Authenticate and create Google Drive service instance
    drive_service = GoogleDriveService().build()
    # Check if model_id folder exists in Google Drive
    folder_query = f"name='{model_id}' and mimeType='application/vnd.google-apps.folder'"
    response = drive_service.files().list(q=folder_query).execute()
    folders = response.get('files', [])
    if not folders:
        raise HTTPException(status_code=404, detail=f"Model not found for model_id: {model_id}")

    # Create tmp/data directory if it doesn't exist
    os.makedirs(os.path.join(TMP_DATA_DIR, model_id), exist_ok=True)

    # Download model.joblib file from Google Drive
    folder_id = folders[0]['id']
    file_query = f"'{folder_id}' in parents and name='model.joblib'"
    response = drive_service.files().list(q=file_query).execute()
    files = response.get('files', [])

    if not files:
        raise HTTPException(status_code=404, detail=f"Model.joblib file not found for model_id: {model_id}")

    file_id = files[0]['id']
    save_path = os.path.join(TMP_DATA_DIR, model_id, "model.joblib")
    request = drive_service.files().get_media(fileId=file_id)
    with open(save_path, 'wb') as f:
        f.write(request.execute())

# Endpoint to predict using a model
@router.post('/download-and-predict/{model_id}')
async def predict(model_id: str, features: dict):
    try:
        model = load_model_from_file(model_id)
    except HTTPException as e:
        if e.status_code == 404:
            try:
                download_model_folder_from_drive(model_id)
                model = load_model_from_file(model_id)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to download and load model: {e}")
        else:
            raise HTTPException(status_code=500, detail=str(e))

    # Make prediction
    try:
        # Convert features to a 2-dimensional matrix
        feature_values = list(features.values())  # Extract feature values
        input_matrix = [feature_values]  # Reshape into a 2D array
        prediction = model.predict(input_matrix)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")

    return {"model_id": model_id, "predictions": prediction.tolist()}