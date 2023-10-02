import io

import torch
from app.utils.repsonse.result import ResultResponse
from extensions.minio import MinioConnector
from fastapi import status
from mmcv import Config
from mmcv.runner import load_checkpoint
from settings import config

from mmfashion.core import AttrPredictor
from mmfashion.models import build_predictor
from mmfashion.utils import get_img_tensor


class AttributePredictCoarseService():
    def __init__ (self, storage: MinioConnector):
        self.checkpoint_path = config["APC_MODEL_SAVING_DIR"]
        self.device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
        self.storage = storage
        self.cfg = Config.fromfile(config["APC_CONFIG_DIR"])
        self.cfg.model.pretrained = None
        self.model = build_predictor(self.cfg.model)
        load_checkpoint(self.model, self.checkpoint_path, map_location='cpu')
        self.model.eval()

    def get_result(self, path_image: str) -> ResultResponse:
        image = self.storage.get_object_from_path(path_image)
        img_io = io.BytesIO(image)
        # image = PILImage.open(img_io).convert('RGB')
        img_tensor = get_img_tensor(
            img_io, 
            use_cuda=False,
        )
        landmark_tensor = torch.zeros(8)

        # predict probabilities for each attribute
        attr_prob = self.model(
            img_tensor, attr=None, landmark=landmark_tensor, return_loss=False)
        attr_predictor = AttrPredictor(self.cfg.data.test)
        result = attr_predictor.show_prediction(attr_prob)
        return ResultResponse((None, status.HTTP_200_OK, result))



