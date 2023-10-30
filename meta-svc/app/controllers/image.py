import base64

from fastapi import APIRouter, Depends, Request, UploadFile

from app.services.image import ImageService
from app.utils.repsonse.result import handle_result
from extensions.keycloak.utils import require_token

router = APIRouter()


@router.post('/', dependencies=[Depends(require_token)])
async def add_images(request: Request, files: list[UploadFile]):
    user_auth = request.state.user_auth
    access_token = user_auth['access_token']
    user_info = request.app.kc_openid.keycloak_openid.userinfo(access_token)
    username = user_info['preferred_username']

    images = {}
    for file in files:
        filename = file.filename
        filename_elements = filename.split('.')
        label, original_image_name = filename_elements[0], '.'.join(filename_elements[1:])
        if label not in images:
            images[label] = [{
                "filename": original_image_name,
                "content": base64.b64encode(await file.read()),
            }]
        else:
            images[label].append({
                "filename": original_image_name,
                "content": base64.b64encode(await file.read()),
            })

    response = ImageService(
        db=request.app.db, 
        storage=request.app.storage
    ).add_images(username, images)
    return handle_result(response)


@router.get('/', dependencies=[Depends(require_token)])
async def get_images(request: Request):
    user_auth = request.state.user_auth
    access_token = user_auth['access_token']
    user_info = request.app.kc_openid.keycloak_openid.userinfo(access_token)
    username = user_info['preferred_username']

    response = ImageService(
        db=request.app.db, 
        storage=request.app.storage
    ).get_images(username)
    return handle_result(response)
