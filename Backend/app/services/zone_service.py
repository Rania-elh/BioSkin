from bson.objectid import ObjectId

class ZoneService:
    def __init__(self, db):
        self.collection = db.zones  # Collection MongoDB "zones"

    def list_zones(self):
        """
        Retourne toutes les zones disponibles.
        """
        zones = list(self.collection.find())
        for zone in zones:
            zone["_id"] = str(zone["_id"])  # Convertit l’ID en string pour JSON
        return zones
