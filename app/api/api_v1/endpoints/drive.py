from fastapi import APIRouter, HTTPException, Path, Request
from app.utils.g_drive_service import GoogleDriveService

import os

router = APIRouter()

@router.get('/gdrive-files')
async def get_file_list_from_gdrive():
    selected_fields = "files(id,name,webViewLink)"
    g_drive_service = GoogleDriveService().build()
    try:
        list_file = g_drive_service.files().list(fields=selected_fields).execute()
        return {"files": list_file.get("files")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/download-model/{folder_path}')
async def download_model(request: Request, folder_path: str = Path(...)):
    # Authenticate and create GoogleDriveService instance
    g_drive_service = GoogleDriveService().build()

    # Get folder ID from the folder path (assuming you have a method to retrieve folder ID)
    folder_id = get_folder_id_from_path(folder_path)

    # Create the folder where the model file will be saved if it doesn't exist
    save_folder = os.path.join('/tmp/data/', folder_path)
    os.makedirs(save_folder, exist_ok=True)

    # Get the list of files in the folder
    folder_files = g_drive_service.files().list(q=f"'{folder_id}' in parents").execute().get('files', [])

    # Find the model file ('model.joblib') in the folder
    model_file = next((file_info for file_info in folder_files if file_info['name'] == 'model.joblib'), None)
    if model_file is None:
        raise HTTPException(status_code=404, detail="Model file 'model.joblib' not found in the specified folder")

    # Download the model file
    file_id = model_file['id']
    save_path = os.path.join(save_folder, 'model.joblib')
    try:
        file = g_drive_service.files().get_media(fileId=file_id).execute()
        with open(save_path, 'wb') as local_file:
            local_file.write(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Model file 'model.joblib' downloaded and saved to 'data' folder"}

def get_folder_id_from_path(folder_path: str) -> str:
    # Parse the file path to extract the file name or any identifier you use
    # For example, if your file path contains the file name directly, you can simply return it
    file_name = folder_path  # Not assuming that folder_path is a URL or a local path
    
    # Use the Google Drive API or any other method to search for the file and retrieve its ID
    # Here, we'll use a mock dictionary to represent a mapping of file names to IDs
    file_id_mapping = {
        "fec38033-68bd-53cf-804c-8c0eb1bc4b95": "1dUQ_qlgXLmjPjWHV4ErhNUJuh8K-kaSz",
        "1ee1e92a-6337-5c24-a377-0738c56ad115": "10Xb8x5R2V6vm5IR-WUPuVezPiPjsnL2c"
    }

    # Check if the file name exists in the mapping
    if file_name in file_id_mapping:
        return file_id_mapping[file_name]
    else:
        # If the file name is not found, raise an error or return a default value
        raise HTTPException(status_code=404, detail=f"Folder '{folder_path}' not found in Google Drive")
