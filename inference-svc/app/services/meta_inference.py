import io
import math
from collections import Counter

import cv2
import matplotlib.colors as mcolors
import numpy as np
import torch
from fastapi import status
from PIL import Image as PILImage
from sklearn.cluster import KMeans
from torchvision import transforms

from app.modeling.meta import ProtoNet
from app.services import AppService
from app.utils.repsonse.result import ResultResponse
from extensions.minio import MinioConnector


class MetaInferenceService(AppService):
    def __init__ (self, config, storage: MinioConnector):
        self.config = config
        checkpoint_path = config["MODEL_SAVING_DIR"]
        self.device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
        # self.model = ProtoNet.load_from_checkpoint(checkpoint_path, map_location=torch.device('cpu'))
        self.storage = storage


    def get_result(self, path_image: str) -> ResultResponse:
        image = self.storage.get_object_from_path(path_image)
        img_io = io.BytesIO(image)
        image = PILImage.open(img_io).convert('RGB')

        image = image.resize((224, 224))
        # tensor_image = transforms.ToTensor()(image).unsqueeze(0)
        # tensor_image = self.model.model(tensor_image.to(self.device))
        # tensor_image = tensor_image.detach().cpu()

        result = {
            "vector": []
        }

        return ResultResponse((None, status.HTTP_200_OK, result))

