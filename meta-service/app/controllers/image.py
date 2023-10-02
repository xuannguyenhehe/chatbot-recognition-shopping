# from fastapi import APIRouter, Depends
# from fastapi.responses import Response
# from app.schemas.inference import InferenceInput
# from app.services.image import ImageService
# from app.utils.repsonse.result import handle_result
# from extensions.minio import get_storage


# router = APIRouter(prefix="/image")

# @router.get('/{path:path}')
# async def get_content_image(path: str, storage: get_storage = Depends()):
#     path = path.replace("image/", "images/")
#     image = ImageService(storage).get_image_content(path)
#     return Response(content=image.read(), media_type="image/png")