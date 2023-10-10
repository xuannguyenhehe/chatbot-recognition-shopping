from fastapi import APIRouter, Request
from fastapi.responses import Response
from app.services.image import ImageService


router = APIRouter(prefix="/image")


@router.get('/{path:path}')
async def get_content_image(request: Request, path: str):
    image = ImageService(
        storage=request.app.storage,
        db=request.app.db,
    ).get_image_content(path)
    return Response(content=image.read(), media_type="image/png")
