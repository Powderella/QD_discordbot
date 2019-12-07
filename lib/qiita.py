"""
    async version Qiita API
"""

import aiohttp
import json

from settings import QIITA_TAG_URL, QIITA_TOKEN

class QiitaTagAPI():
    def __init__(self, tag=None, page=1, per_page=10):
        self.qiita_query = {
            "page": page,
            "per_page": per_page,
        }
        self.tag = tag
        
    async def _fetchJson(self, url, session, headers=str()):
        async with session.get(url, headers=headers, params=self.qiita_query) as r:
            r.raise_for_status()
            return await r.json()
    
    async def fetchArticlesFromTag(self, item_num=5):
        """
        """
        headers = {
            "charset": "utf-8",
            "Authorization": f"Bearer {QIITA_TOKEN}"
        }
        url = QIITA_TAG_URL.format(self.tag)

        async with aiohttp.ClientSession() as session:
            json = await self._fetchJson(url, session, headers)
            return {self.tag: [self._purseJson(j) for j in json[0:item_num]]}
    
    def _purseJson(self, json, article_query=["title", "url", "created_at"]):
        """
        qiita query param:['rendered_body', 'body', 'coediting',
                        'comments_count', 'created_at', 'group',
                        'id', 'likes_count', 'private',
                        'reactions_count','tags', 'title', 
                        'updated_at', 'url', 'user', 
                        'page_views_count']
        """
        return {k:json[k] for k in json.keys() if k in article_query}
