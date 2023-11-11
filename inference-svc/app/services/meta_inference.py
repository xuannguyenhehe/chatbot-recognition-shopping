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
            "vector": torch.tensor([[
                -0.1009, -0.0602, -0.1614, -0.0527, -0.0360,  0.1156,  0.0199, -0.0645,
                0.0148,  0.1509, -0.1255, -0.2595, -0.0456,  0.1277, -0.0135, -0.1287,
                0.1169, -0.1971,  0.1092,  0.0143,  0.2096,  0.0801, -0.0568,  0.0706,
                -0.1224,  0.0076,  0.0198,  0.0237,  0.0584, -0.0562,  0.0685,  0.0173,
                -0.0220, -0.1131, -0.0861, -0.0189, -0.0648,  0.2133,  0.0848,  0.0333,
                -0.0307, -0.0477, -0.0347,  0.0073, -0.1457, -0.0984, -0.0034, -0.0200,
                0.0719, -0.0641, -0.1282, -0.0148,  0.0246,  0.0144,  0.1513,  0.0383,
                0.1072, -0.0439,  0.0267, -0.0453, -0.0619,  0.1715, -0.0707, -0.0274
            ]]).tolist()
        }

        return ResultResponse((None, status.HTTP_200_OK, result))
