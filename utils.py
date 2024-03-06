import os
from pprint import pprint
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


async def get_shopping_list(bot):
    res = request(url=f"{os.getenv('NOTION_BASE_URL')}blocks/{os.getenv('SHOP_LIST_ID')}/children?page_size=100 ",
                  method="GET",
                  headers=get_headers(user_id=int(os.getenv('MY_ID'))))

    shopping_list = "🛒 Список покупок:\n"
    for item in res.json()['results']:
        if not item['to_do']['checked']:
            shopping_list += '- ' + item['to_do']['rich_text'][0]['plain_text'] + '\n'

    await bot.send_message(os.getenv('MY_ID'), shopping_list)
