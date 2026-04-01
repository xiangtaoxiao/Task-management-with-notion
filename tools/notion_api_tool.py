import os
import json
from notion_client import Client
from dotenv import load_dotenv

class NotionAPITool:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("NOTION_API_KEY")
        if not self.api_key:
            raise ValueError("Notion API key is required")
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
