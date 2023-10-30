import io
import math
from collections import Counter

import cv2
import matplotlib.colors as mcolors
import numpy as np
from fastapi import status
from PIL import Image as PILImage
from sklearn.cluster import KMeans

from app.services import AppService
from app.utils.repsonse.result import ResultResponse
from extensions.minio import MinioConnector


class ColorInferenceService(AppService):
    def __init__ (self, config, storage: MinioConnector):
        self.config = config
        self.storage = storage


    def get_colors(self, path_image: str, k: int = 5):
        image = self.storage.get_object_from_path(path_image)
        img_io = io.BytesIO(image)
        image = PILImage.open(img_io).convert('RGB')
        colors = self._get_color_image(image)
        return ResultResponse((None, status.HTTP_200_OK, colors))

    def _get_color_image(self, image, k: int = 3):
        colors = self.config["IMAGE_COLORS"].split(",")
        number_of_colors = len(colors)
        if k > number_of_colors:
            return []
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        image = self._crop_img(image, 0.2)
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
            results.append(self._get_dist(
                tuple([c*255 for c in mcolors.to_rgb(c_name)]), 
                np.array(rgb_colors).mean(axis=0))
            )
        idxs = sorted(range(len(results)), key=lambda i: results[i])[:k]
        result_colors = [colors[idx] for idx in idxs]
        return result_colors
    
    def _crop_img(self, img, scale=1.0):
        center_x, center_y = img.shape[1] / 2, img.shape[0] / 2
        width_scaled, height_scaled = img.shape[1] * scale, img.shape[0] * scale
        left_x, right_x = center_x - width_scaled / 2, center_x + width_scaled / 2
        top_y, bottom_y = center_y - height_scaled / 2, center_y + height_scaled / 2
        img_cropped = img[int(top_y):int(bottom_y), int(left_x):int(right_x)]
        return img_cropped

    def _get_dist(self, color1, color2):
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        d=math.sqrt((r2-r1)**2+(g2-g1)**2+(b2-b1)**2)
        p=d/math.sqrt((255)**2+(255)**2+(255)**2)
        return p
