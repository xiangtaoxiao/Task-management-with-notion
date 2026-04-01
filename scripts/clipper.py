import os
import json
import sys
from notion_client import Client

class NotionClipper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = Client(auth=self.api_key)
    
    def clip_webpage(self, url, title, content, tags=None):
        """Clip webpage content to Notion"""
        try:
            # Load configuration
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            
            database_id = config.get("database_id")
            if not database_id:
                return {
                    "status": "error",
                    "message": "Database ID not found. Please initialize Notion first."
                }
            
            # Create page properties
            properties = {
                "待办事项": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                },
                "备注": {
                    "rich_text": [
                        {
                            "text": {
                                "content": f"URL: {url}\n\n{content}"
                            }
                        }
                    ]
                },
                "类别": {
                    "select": {
                        "name": "学习"
                    }
                },
                "状态": {
                    "status": {
                        "name": "待办"
                    }
                }
            }
            
            # Add tags if provided
            if tags:
                properties["备注"]["rich_text"].append({
                    "text": {
                        "content": f"\n\nTags: {', '.join(tags)}"
                    }
                })
            
            # Create page
            response = self.client.pages.create(
                parent={"database_id": database_id},
                properties=properties
            )
            
            return {
                "status": "success",
                "message": "Webpage clipped successfully",
                "page_id": response.get("id")
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Clipping failed: {str(e)}"
            }
    
    def clip_text(self, text, title, tags=None):
        """Clip text content to Notion"""
        try:
            # Load configuration
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            
            database_id = config.get("database_id")
            if not database_id:
                return {
                    "status": "error",
                    "message": "Database ID not found. Please initialize Notion first."
                }
            
            # Create page properties
            properties = {
                "待办事项": {
                    "title": [
                        {
                            "text": {
                                "content": title
                            }
                        }
                    ]
                },
                "备注": {
                    "rich_text": [
                        {
                            "text": {
                                "content": text
                            }
                        }
                    ]
                },
                "类别": {
                    "select": {
                        "name": "学习"
                    }
                },
                "状态": {
                    "status": {
                        "name": "待办"
                    }
                }
            }
            
            # Add tags if provided
            if tags:
                properties["备注"]["rich_text"].append({
                    "text": {
                        "content": f"\n\nTags: {', '.join(tags)}"
                    }
                })
            
            # Create page
            response = self.client.pages.create(
                parent={"database_id": database_id},
                properties=properties
            )
            
            return {
                "status": "success",
                "message": "Text clipped successfully",
                "page_id": response.get("id")
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Clipping failed: {str(e)}"
            }

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({
            "status": "error",
            "message": "Missing command or arguments. Usage: python clipper.py <command> [args]"
        }))
        sys.exit(1)
    
    command = sys.argv[1]
    
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
    
    clipper = NotionClipper(api_key)
    
    if command == "webpage":
        if len(sys.argv) < 5:
            print(json.dumps({
                "status": "error",
                "message": "Missing url, title, or content"
            }))
            sys.exit(1)
        url = sys.argv[2]
        title = sys.argv[3]
        content = sys.argv[4]
        tags = sys.argv[5].split(",") if len(sys.argv) > 5 else None
        result = clipper.clip_webpage(url, title, content, tags)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "text":
        if len(sys.argv) < 4:
            print(json.dumps({
                "status": "error",
                "message": "Missing title or content"
            }))
            sys.exit(1)
        title = sys.argv[2]
        content = sys.argv[3]
        tags = sys.argv[4].split(",") if len(sys.argv) > 4 else None
        result = clipper.clip_text(content, title, tags)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    else:
        print(json.dumps({
            "status": "error",
            "message": f"Unknown command: {command}"
        }))
        sys.exit(1)
