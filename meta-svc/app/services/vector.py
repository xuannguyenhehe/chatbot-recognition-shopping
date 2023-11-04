from typing import List, Tuple

from app.models.image import Image
from app.models.vector import Vector
from app.services import AppCRUD


class VectorCRUD(AppCRUD):
    def create(self, vector: Vector) -> Tuple:
        vector = Vector(**vector.dict())
        message, status_code = self.insert("Vector", self.serialize(vector))
        return message, status_code
    
    def get_by_username(self, username: str):
        query = {
            "username": username,
        }
        no_query = {
            "_id": False,
            "is_active": False,
            "created_date": False,
            "updated_date": False,
        }
        vector = list(self.db.Vector.find(query, no_query))[0]
        return vector
