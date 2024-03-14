from fastapi import APIRouter

from .endpoints import drive
from .endpoints import modelPredict

router = APIRouter()
router.include_router(drive.router, prefix="/drive", tags=["GoogleDrive"])
router.include_router(modelPredict.router, prefix="/models", tags=["Models"])