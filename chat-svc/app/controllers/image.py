from fastapi import APIRouter, Depends
from fastapi.responses import Response
from app.services.image import ImageService
from extensions.minio import get_storage
from app.models import get_database


router = APIRouter(prefix="/image")

@router.get('/{path:path}')
async def get_content_image(
    path: str, 
    storage: get_storage = Depends(),
    db: get_database = Depends(),
):
    image = ImageService(
        storage=storage,
        db=db,
    ).get_image_content(path)
    return Response(content=image.read(), media_type="image/png")
