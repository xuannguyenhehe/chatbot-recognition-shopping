import io

import numpy as np
import torch
from app.modeling import ProtoNet
from app.schemas.inference import InferenceInput
from app.services import AppService
from app.services.image import ImageCRUD
from app.utils.repsonse.result import ResultResponse
from config import config
from extensions.minio import MinioConnector
from fastapi import status
from PIL import Image as PILImage
from torchvision import transforms

import cv2
from sklearn.cluster import KMeans
from collections import Counter
import math 
import matplotlib.colors as mcolors


class InferenceService(AppService):
    def __init__ (self, storage: MinioConnector, vector_search, db):
        checkpoint_path = config["MODEL_SAVING_DIR"]
        self.device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
        self.model = ProtoNet.load_from_checkpoint(checkpoint_path, map_location=torch.device('cpu'))
        self.storage = storage
        self.vector_search = vector_search
        self.db = db

    def get_result(self, input: InferenceInput, k: int = 5) -> ResultResponse:
        path_image = input.path_image
        entities = input.entities
        require_cates = [entity["value"] for entity in entities if entity["entity"] == "cate"]
        require_attrs = [entity["value"] for entity in entities if entity["entity"] == "attr"]
        require_colors = [entity["value"] for entity in entities if entity["entity"] == "color"]
        results = []

        if path_image:
            image = self.storage.get_object_from_path(path_image)
            img_io = io.BytesIO(image)
            image = PILImage.open(img_io).convert('RGB')

            if len(entities) > 0:
                cate, attr = self.get_info_cate_attr_image(path_image)
                color = self.get_color_image(image)

            image = image.resize((224, 224))
            tensor_image = transforms.ToTensor()(image).unsqueeze(0)
            tensor_image = self.model.model(tensor_image.to(self.device))
            tensor_image = tensor_image.detach().cpu()
            dist = torch.pow(self.vector_search - tensor_image, 2).sum(dim=2)
            dist_shape = dist.shape

            query_old = 0
            query_new = k
            while len(results) < 5:
                _, i = torch.topk(dist.flatten(), query_new, largest=False)
                topk_positions = np.array(np.unravel_index(i.numpy(), dist.shape)).T
                for num_1, num_2 in topk_positions[:-(query_new - query_old)]:
                    full_index = num_1 * dist_shape[1] + num_2
                    index_label = full_index // dist_shape[0]
                    index_image_in_label = full_index % dist_shape[0]
                    path_image, cate_image, attr_image, color_image = ImageCRUD(self.db)\
                                            .get_by_index(index_label, index_image_in_label)
                    common_cate = set(cate["top 5"]).intersection(cate_image["top 5"])
                    common_attr = set(attr["top 10"]).intersection(attr_image["top 10"])
                    common_color = set(color).intersection(color_image)
                    if len(common_cate) > 0 and len(common_attr) > 0 and len(common_color) > 0:
                        results.append(path_image)
                query_old += query_new
                query_new += (k - len(results))
        else:
            images = ImageCRUD(self.db).query_by_cate_attr_color(
                cate=require_cates,
                attr=require_attrs,
                color=require_colors,
                k=k,
            )
            results = [image["path"] for image in images]

        return ResultResponse((None, status.HTTP_200_OK, results))
    
    def get_info_cate_attr_image(self, path_image: str):
        url = "/api/mmfashion-service/v1/cap"
        payload = {
            "path_image": path_image,
        }
        data, _ = self.call_api(url, payload, "post")
        attr = data["attr"]
        cate = data["cate"]
        return cate, attr

    def get_color_image(self, image, k: int = 3):
        colors = config["IMAGE_COLORS"]
        number_of_colors = len(colors)
        if k > number_of_colors:
            return []
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        image = self.crop_img(image, 0.2)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        modified_image = image.reshape(image.shape[0]*image.shape[1], 3)
        clf = KMeans(n_clusters = number_of_colors)
        labels = clf.fit_predict(modified_image)
        counts = Counter(labels)
        center_colors = clf.cluster_centers_
        ordered_colors = [center_colors[i] for i in counts.keys()]
        rgb_colors = [ordered_colors[i] for i in counts.keys()]
        results = []
        for c_name in colors:
            results.append(self.get_dist(
                tuple([c*255 for c in mcolors.to_rgb(c_name)]), 
                np.array(rgb_colors).mean(axis=0))
            )
        idxs = sorted(range(len(results)), key=lambda i: results[i])[:k]
        result_colors = [colors[idx] for idx in idxs]
        return result_colors
    
    def crop_img(self, img, scale=1.0):
        center_x, center_y = img.shape[1] / 2, img.shape[0] / 2
        width_scaled, height_scaled = img.shape[1] * scale, img.shape[0] * scale
        left_x, right_x = center_x - width_scaled / 2, center_x + width_scaled / 2
        top_y, bottom_y = center_y - height_scaled / 2, center_y + height_scaled / 2
        img_cropped = img[int(top_y):int(bottom_y), int(left_x):int(right_x)]
        return img_cropped

    def get_dist(self, color1, color2):
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        d=math.sqrt((r2-r1)**2+(g2-g1)**2+(b2-b1)**2)
        p=d/math.sqrt((255)**2+(255)**2+(255)**2)
        return p