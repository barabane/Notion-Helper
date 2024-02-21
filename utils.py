import os
from requests import request
from dotenv import load_dotenv

load_dotenv()


def get_headers(user_id: int):
    return {
        'Authorization': f"Bearer {os.getenv('NOTION_SECRET') if str(user_id) == os.getenv('MY_ID') else os.getenv('NOTION_SECRET_P')}",
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
    }


def add_link(user_id: int, text: str):
    res = request(url=f"{os.getenv('NOTION_BASE_URL')}pages",
                  method="POST", headers=get_headers(user_id=user_id), json={
            "parent": {
                "database_id": os.getenv('DB_ID') if str(user_id) == os.getenv('MY_ID') else os.getenv('DB_ID_P')
            },
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": "Ссылка"
                            }
                        }
                    ]
                },
            },
            "children": [
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": f"{text}",
                                    "link": {
                                        "url": f"{text}"
                                    }
                                }
                            }]
                    }
                }]
        })

    return res


def add_page(user_id: int, text: str):
    res = request(url=f"{os.getenv('NOTION_BASE_URL')}pages",
                  method="POST", headers=get_headers(user_id=user_id), json={
            "parent": {
                "database_id": os.getenv('DB_ID') if str(user_id) == os.getenv('MY_ID') else os.getenv('DB_ID_P')
            },
            "properties": {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": f"{text}"
                            }
                        }
                    ]
                },
            }
        })

    return res
