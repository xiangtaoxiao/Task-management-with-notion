import json
import os
from tools.notion_api_tool import NotionAPITool
from tools.storage_tool import StorageTool

class NotionInitSkill:
    def __init__(self):
        self.storage = StorageTool()
    
    def run(self, api_key):
        """Run the initialization process"""
        try:
            # Initialize Notion API tool
            notion = NotionAPITool(api_key)
            
            # Search for existing database
            database_name = "To Do List 任务看板"
            existing_db = notion.search_database(database_name)
            
            if existing_db:
                database_id = existing_db["id"]
                message = f"Found existing database: {database_name}"
            else:
                # Create a new page as parent for the database
                # First, search for any existing page
                has_more = True
                start_cursor = None
                parent_page_id = None
                
                while has_more and not parent_page_id:
                    response = notion.client.search(
                        query="",
                        filter={"property": "object", "value": "page"},
                        start_cursor=start_cursor
                    )
                    
                    for result in response["results"]:
                        if "id" in result:
                            parent_page_id = result["id"]
                            break
                    
                    has_more = response["has_more"]
                    start_cursor = response["next_cursor"]
                
                if not parent_page_id:
                    return {
                        "status": "error",
                        "message": "No existing pages found to use as parent for database",
                        "database_id": None,
                        "database_name": database_name
                    }
                
                # Create new database
                new_db = notion.create_database(parent_page_id, database_name)
                database_id = new_db["id"]
                message = f"Created new database: {database_name}"
            
            # Save configuration
            self.storage.save_user_config({"api_key": api_key})
            self.storage.save_database_id(database_id)
            
            return {
                "status": "success",
                "message": message,
                "database_id": database_id,
                "database_name": database_name
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Initialization failed: {str(e)}",
                "database_id": None,
                "database_name": "To Do List 任务看板"
            }

if __name__ == "__main__":
    # For testing
    import sys
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
        skill = NotionInitSkill()
        result = skill.run(api_key)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Please provide Notion API key as argument")
