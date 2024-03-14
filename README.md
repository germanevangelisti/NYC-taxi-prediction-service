# NYC Taxi Prediction Service
This service provides functionalities to interact with models and data stored in Google Drive for predicting NYC taxi trip details based on certain features. It is built using FastAPI, a modern web framework for building APIs with Python.


## Features

-   **Google Drive Integration**: Allows users to list files and download models from Google Drive.
-   **Model Prediction**: Provides an endpoint to make predictions using pre-trained models.

## Requirements

-   Python 3.7+
-   FastAPI
-   g_drive_service
-   joblib
-   numpy
-   pydantic

## Installation

Clone the repository:

`git clone https://github.com/yourusername/NYC-taxi-prediction-service.git
cd NYC-taxi-prediction-service` 

## Usage

### Locally


1.  Install the dependencies:

`pip install -r requirements.txt`

2.  Start the FastAPI server:

`uvicorn main:app --reload` 

3.  Access the interactive API documentation at `http://127.0.0.1:80/docs` to explore available endpoints and make requests.

### with Docker

1. build docker image
`docker build -t nyc-taxi-prediction-service:latest -f Dockerfile .`

2. run docker container
`docker run -d -p 80:80 nyc-taxi-prediction-service:latest`

## Endpoints

-   **GET drive/gdrive-files**: Lists files in Google Drive.
-   **GET drive/download-model/{folder_path}**: Downloads a model file from a specified folder in Google Drive.
-   **POST models/predict/{model_id}**: Makes predictions using a specified model.
-   **POST models/download-and-predict/{model_id}**: Downloads the model if does not exists in temp/data folder and makes predictions using the specified model.

## Configuration

Before running the service, ensure that you have set up the required configurations:

-   **Google Drive API Credentials**: Place your Google Drive API credentials (`credentials.json`) in the root directory of the project.

## Test with POSTMAN

-   **GET:  http://localhost:80/api/v1/drive/gdrive-files
-   **GET:  http://localhost:80/api/v1/drive/download-model/fec38033-68bd-53cf-804c-8c0eb1bc4b95
-   **POST: http://localhost:80/api/v1/models/predict/fec38033-68bd-53cf-804c-8c0eb1bc4b95
-   **POST: http://localhost:80/api/v1/models/download-and-predict/fec38033-68bd-53cf-804c-8c0eb1bc4b95
-   **body: 
				{
					"trip_distance": 10,
					"diff_seconds": 100,
					"day_num": 2,
					"hour": 12
				}