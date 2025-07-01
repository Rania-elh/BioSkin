from bson.objectid import ObjectId

class SkinTypeService:
    def __init__(self, db):
        self.collection = db.skin_types  # Collection MongoDB "skin_types"

    def list_skin_types(self):
        """
        Retourne tous les types de peau disponibles.
        """
        skin_types = list(self.collection.find())
        for skin_type in skin_types:
            skin_type["_id"] = str(skin_type["_id"])  # Conversion de l'ID
        return skin_types
