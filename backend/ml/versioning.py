import json
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ModelVersionManager:
    def __init__(self, metadata_path="models/model_metadata.json"):
        self.metadata_path = metadata_path
        self.metadata = self.load_metadata()

    def load_metadata(self):
        if os.path.exists(self.metadata_path):
            with open(self.metadata_path, 'r') as f:
                return json.load(f)
        return {"versions": []}

    def save_metadata(self):
        with open(self.metadata_path, 'w') as f:
            json.dump(self.metadata, f, indent=4)

    def register_model(self, model_type, metrics, features, algorithm="xgboost", parameters=None):
        version_num = len(self.metadata["versions"]) + 1
        version_id = f"MODEL_V{version_num}"
        
        entry = {
            "model_version": version_id,
            "model_type": model_type,
            "training_timestamp": datetime.now().isoformat(),
            "algorithm": algorithm,
            "parameters": parameters or {},
            "features": features,
            "metrics": metrics,
            "status": "ACTIVE"
        }
        
        # Deactivate previous active models of same type
        for v in self.metadata["versions"]:
            if v["model_type"] == model_type and v["status"] == "ACTIVE":
                v["status"] = "ARCHIVED"
                
        self.metadata["versions"].append(entry)
        self.save_metadata()
        logger.info(f"Registered new model version: {version_id}")
        return version_id
        
    def get_active_model(self, model_type):
        for v in reversed(self.metadata["versions"]):
            if v["model_type"] == model_type and v["status"] == "ACTIVE":
                return v
        return None

version_manager = ModelVersionManager()
