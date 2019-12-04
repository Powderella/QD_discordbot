"""
    Qiita API
"""

import requests
import json
import shelve

from settings import QIITA_TAG_URL, QIITA_TOKEN

class QiitaTagAPI():
    def __init__(self, page=1, per_page=10):
        self.query = {
            "page": page,
            "per_page": per_page,
        }
    
    def getArticlesFromTags(self, tags=list, item_num=5, query=["title", "url"]):
        """
        query param:['rendered_body', 'body', 'coediting',
                    'comments_count', 'created_at', 'group',
                    'id', 'likes_count', 'private',
                    'reactions_count','tags', 'title', 
                    'updated_at', 'url', 'user', 
                    'page_views_count']
        return list(dict())
        """
        articlesDict = {}
        urls = [QIITA_TAG_URL.format(tag) for tag in tags]
        headers = {
            "charset": "utf-8",
            "Authorization": f"Bearer {QIITA_TOKEN}"
        }

        for url, tag in zip(urls,tags):
            response = requests.get(url, params=self.query, headers=headers)
            response.raise_for_status()
            
            articles = response.json()[0:item_num]

            trashElem = [k for k in articles[0] if k not in query]
            
            for i in range(item_num):
                for k in trashElem:
                    del articles[i][k]

            
            articlesDict[tag] = articles
        return articlesDict
                
    def writeFavoriteArticleInMyDB(self, tag):
        with shelve.open("QiitaFavoriteArticle") as db:
            db[tag] = tag
    
if __name__ == "__main__":
    qtapi = QiitaTagAPI()
    articles = qtapi.getArticlesFromTags(["Python", "C"], 5)
    for k, v in articles.items():
        print(k, v)