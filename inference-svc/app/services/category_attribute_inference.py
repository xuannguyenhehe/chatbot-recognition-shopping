import io

import torch
from fastapi import status
from mmcv import Config
from mmcv.runner import load_checkpoint

from app.modeling.mmfashion.core import AttrPredictor, CatePredictor
from app.modeling.mmfashion.models import build_predictor
from app.modeling.mmfashion.utils import get_img_tensor
from app.utils.repsonse.result import ResultResponse
from extensions.minio import MinioConnector


class CategoryAttributePredictService():
    def __init__ (self, storage: MinioConnector, config):
        self.checkpoint_path = config["CAP_MODEL_SAVING_DIR"]
        self.device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
        self.storage = storage
        self.cfg = Config.fromfile(config["CAP_CONFIG_DIR"])
        self.cfg.model.pretrained = None
        self.model = build_predictor(self.cfg.model)
        # load_checkpoint(self.model, self.checkpoint_path, map_location='cpu')
        # self.model.eval()

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
        # attr_prob, cate_prob = self.model(
        #     img_tensor, attr=None, landmark=landmark_tensor, return_loss=False)
        attr_predictor = AttrPredictor(self.cfg.data.test)
        cate_predictor = CatePredictor(self.cfg.data.test)
        # result_attr = attr_predictor.show_prediction(attr_prob)
        result_attr = attr_predictor.get_random()
        result_cate = cate_predictor.get_random()
        # result_cate = cate_predictor.show_prediction(cate_prob)
        return ResultResponse((None, status.HTTP_200_OK, {
            "attr": result_attr,
            "cate": result_cate,
        }))