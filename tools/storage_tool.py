import os
import json
import yaml

class StorageTool:
    def __init__(self, storage_type="local", path="./storage"):
        self.storage_type = storage_type
        self.path = path
        
        if storage_type == "local":
            os.makedirs(path, exist_ok=True)
            self.config_file = os.path.join(path, "config.json")
            self.database_file = os.path.join(path, "database.json")
    
    def save_user_config(self, config):
        """Save user configuration"""
        if self.storage_type == "local":
            # Load existing config if it exists
            existing_config = self.get_user_config() or {}
            # Update with new config
            existing_config.update(config)
            # Save to file
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(existing_config, f, indent=2, ensure_ascii=False)
            return True
        return False
    
    def get_user_config(self):
        """Get user configuration"""
        if self.storage_type == "local":
            if os.path.exists(self.config_file):
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
        return {}
    
    def save_database_id(self, database_id):
        """Save database ID"""
        if self.storage_type == "local":
            data = {"database_id": database_id}
            with open(self.database_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        return False
    
    def get_database_id(self):
        """Get database ID"""
        if self.storage_type == "local":
            if os.path.exists(self.database_file):
                with open(self.database_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("database_id")
        return None
    
    def load_config_yaml(self, config_path):
        """Load configuration from YAML file"""
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {}
    
    def save_config_yaml(self, config_path, config):
        """Save configuration to YAML file"""
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        return True
