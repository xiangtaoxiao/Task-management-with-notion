import os
import json
import sys
from notion_client import Client

class NotionClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = Client(auth=self.api_key)
    
    def search_database(self, database_name):
        """Search for a database by name"""
        has_more = True
        start_cursor = None
        
        while has_more:
            response = self.client.search(
                query=database_name,
                filter={"property": "object", "value": "database"},
                start_cursor=start_cursor
            )
            
            for result in response["results"]:
                if "title" in result and result["title"]:
                    db_title = "".join([text["plain_text"] for text in result["title"]])
                    if db_title == database_name:
                        return result
            
            has_more = response["has_more"]
            start_cursor = response["next_cursor"]
        
        return None
    
    def create_database(self, parent_page_id, database_name):
        """Create a new database"""
        properties = {
            "待办事项": {
                "type": "title",
                "title": {}
            },
            "备注": {
                "type": "rich_text",
                "rich_text": {}
            },
            "类别": {
                "type": "select",
                "select": {
                    "options": [
                        {"name": "学习", "color": "blue"},
                        {"name": "生活", "color": "green"},
                        {"name": "工作", "color": "red"}
                    ]
                }
            },
            "状态": {
                "type": "status",
                "status": {
                    "options": [
                        {"name": "待办", "color": "gray"},
                        {"name": "进行中", "color": "blue"},
                        {"name": "已完成", "color": "green"},
                        {"name": "已取消", "color": "red"}
                    ]
                }
            },
            "四象限": {
                "type": "select",
                "select": {
                    "options": [
                        {"name": "重要紧急", "color": "red"},
                        {"name": "重要不紧急", "color": "orange"},
                        {"name": "紧急不重要", "color": "yellow"},
                        {"name": "不重要不紧急", "color": "gray"}
                    ]
                }
            },
            "截止日期": {
                "type": "date",
                "date": {}
            }
        }
        
        response = self.client.databases.create(
            parent={"page_id": parent_page_id},
            title=[{"type": "text", "text": {"content": database_name}}],
            properties=properties
        )
        
        return response
    
    def query_database(self, database_id, filter=None, sorts=None):
        """Query database with optional filter and sorts"""
        has_more = True
        start_cursor = None
        results = []
        
        while has_more:
            response = self.client.databases.query(
                database_id=database_id,
                filter=filter,
                sorts=sorts,
                start_cursor=start_cursor
            )
            results.extend(response["results"])
            has_more = response["has_more"]
            start_cursor = response["next_cursor"]
        
        return results
    
    def create_page(self, database_id, properties):
        """Create a new page in database"""
        response = self.client.pages.create(
            parent={"database_id": database_id},
            properties=properties
        )
        return response
    
    def update_page(self, page_id, properties):
        """Update an existing page"""
        response = self.client.pages.update(
            page_id=page_id,
            properties=properties
        )
        return response
    
    def delete_page(self, page_id):
        """Delete a page (archive it)"""
        response = self.client.pages.update(
            page_id=page_id,
            archived=True
        )
        return response
    
    def get_page(self, page_id):
        """Get a page by ID"""
        response = self.client.pages.retrieve(page_id=page_id)
        return response
    
    def get_block_children(self, block_id):
        """Get children of a block"""
        has_more = True
        start_cursor = None
        children = []
        
        while has_more:
            response = self.client.blocks.children.list(
                block_id=block_id,
                start_cursor=start_cursor
            )
            children.extend(response["results"])
            has_more = response["has_more"]
            start_cursor = response["next_cursor"]
        
        return children
    
    def init_notion(self, api_key):
        """Initialize Notion connection and create database"""
        try:
            # Search for existing database
            database_name = "To Do List 任务看板"
            existing_db = self.search_database(database_name)
            
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
                    response = self.client.search(
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
                new_db = self.create_database(parent_page_id, database_name)
                database_id = new_db["id"]
                message = f"Created new database: {database_name}"
            
            # Save configuration
            config = {
                "api_key": api_key,
                "database_id": database_id,
                "database_name": database_name
            }
            
            # Save to config file
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
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
    
    def manage_task(self, action, task_data):
        """Manage tasks (create, update, delete)"""
        try:
            # Load configuration
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            
            database_id = config.get("database_id")
            if not database_id:
                return {
                    "status": "error",
                    "message": "Database ID not found. Please initialize Notion first.",
                    "data": None
                }
            
            if action == "create":
                response = self.create_page(database_id, task_data)
                return {
                    "status": "success",
                    "message": "Task created successfully",
                    "data": response
                }
            elif action == "update":
                page_id = task_data.get("page_id")
                if not page_id:
                    return {
                        "status": "error",
                        "message": "Page ID is required for update",
                        "data": None
                    }
                # Remove page_id from properties
                properties = {k: v for k, v in task_data.items() if k != "page_id"}
                response = self.update_page(page_id, properties)
                return {
                    "status": "success",
                    "message": "Task updated successfully",
                    "data": response
                }
            elif action == "delete":
                page_id = task_data.get("page_id")
                if not page_id:
                    return {
                        "status": "error",
                        "message": "Page ID is required for delete",
                        "data": None
                    }
                response = self.delete_page(page_id)
                return {
                    "status": "success",
                    "message": "Task deleted successfully",
                    "data": response
                }
            else:
                return {
                    "status": "error",
                    "message": f"Unknown action: {action}",
                    "data": None
                }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Task management failed: {str(e)}",
                "data": None
            }
    
    def query_tasks(self, filter=None, sort=None):
        """Query tasks from database"""
        try:
            # Load configuration
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            
            database_id = config.get("database_id")
            if not database_id:
                return {
                    "status": "error",
                    "message": "Database ID not found. Please initialize Notion first.",
                    "tasks": []
                }
            
            results = self.query_database(database_id, filter, sort)
            
            # Format tasks for output
            tasks = []
            for result in results:
                task = {
                    "id": result.get("id"),
                    "properties": result.get("properties", {})
                }
                tasks.append(task)
            
            return {
                "status": "success",
                "message": f"Found {len(tasks)} tasks",
                "tasks": tasks
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Task query failed: {str(e)}",
                "tasks": []
            }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "error",
            "message": "Missing command. Usage: python notion_client.py <command> [args]"
        }))
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "init":
        if len(sys.argv) < 3:
            print(json.dumps({
                "status": "error",
                "message": "Missing API key"
            }))
            sys.exit(1)
        api_key = sys.argv[2]
        client = NotionClient(api_key)
        result = client.init_notion(api_key)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "task":
        if len(sys.argv) < 4:
            print(json.dumps({
                "status": "error",
                "message": "Missing action or task data"
            }))
            sys.exit(1)
        action = sys.argv[2]
        task_data_str = sys.argv[3]
        try:
            task_data = json.loads(task_data_str)
        except json.JSONDecodeError:
            print(json.dumps({
                "status": "error",
                "message": "Invalid task data JSON"
            }))
            sys.exit(1)
        # Load API key from config
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            api_key = config.get("api_key")
            if not api_key:
                print(json.dumps({
                    "status": "error",
                    "message": "API key not found. Please initialize Notion first."
                }))
                sys.exit(1)
        except FileNotFoundError:
            print(json.dumps({
                "status": "error",
                "message": "Config file not found. Please initialize Notion first."
            }))
            sys.exit(1)
        client = NotionClient(api_key)
        result = client.manage_task(action, task_data)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "query":
        filter_str = sys.argv[2] if len(sys.argv) > 2 else "{}"
        sort_str = sys.argv[3] if len(sys.argv) > 3 else "{}"
        try:
            filter = json.loads(filter_str)
            sort = json.loads(sort_str)
        except json.JSONDecodeError:
            print(json.dumps({
                "status": "error",
                "message": "Invalid filter or sort JSON"
            }))
            sys.exit(1)
        # Load API key from config
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            api_key = config.get("api_key")
            if not api_key:
                print(json.dumps({
                    "status": "error",
                    "message": "API key not found. Please initialize Notion first."
                }))
                sys.exit(1)
        except FileNotFoundError:
            print(json.dumps({
                "status": "error",
                "message": "Config file not found. Please initialize Notion first."
            }))
            sys.exit(1)
        client = NotionClient(api_key)
        result = client.query_tasks(filter, sort)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        print(json.dumps({
            "status": "error",
            "message": f"Unknown command: {command}"
        }))
        sys.exit(1)
