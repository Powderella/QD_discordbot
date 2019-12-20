import aiohttp
from bs4 import BeautifulSoup
import json
import asyncio

class NiconicoVideo:
    """async/await

    """
    def __init__(self, url):
        self.url = url
        self._isOldDouga = False
    
    async def _fetchDougaInfo(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                content = await response.content.read()
        return BeautifulSoup(content, "html.parser")

        
    async def _parseInfo(self):
        soup = await self._fetchDougaInfo()
        init_data = soup.find("div", id="js-initial-watch-data")
        s = str(init_data)[20:-1704].replace("&quot;", '"')
        dmcInfo = json.loads(s)
        videoInfo = dmcInfo["video"]

        if videoInfo.get("dmcInfo") is None:
            info = videoInfo["smileInfo"]["url"]
            self._isOldDouga = True
        else:
            info = videoInfo["dmcInfo"]["session_api"]
            self._isOldDouga = False

        return info

    async def loginNico(self, session, mailAddr=None, password=None):
        """niconicoにログイン
        """
        login_url = "https://account.nicovideo.jp/api/v1/login"
        account = {
            "mail_tel": mailAddr,
            "password": password,
        }
        response = await session.post(login_url, data=account)
        response.raise_for_status()

    
    async def getDownloadUrl(self, session):
        d = await self._parseInfo()
        
        if self._isOldDouga is True:
            return d

        payload = {"session": {
                "recipe_id": d["recipe_id"],
                "content_id": d["content_id"],
                "content_type": "movie",
                "content_src_id_sets": [
                    {
                        "content_src_ids": [
                                {
                                "src_id_to_mux": {
                                    "video_src_ids": d["videos"],
                                    "audio_src_ids": d["audios"]
                                }
                            }
                        ]
                    }
                ],
                "timing_constraint": "unlimited",
                "keep_method": {
                    "heartbeat": {
                        "lifetime": d["heartbeat_lifetime"]
                    }
                },
                "protocol": {
                    "name": "http",
                    "parameters": {
                        "http_parameters": {
                            "parameters": {
                                "http_output_download_parameters": {
                                    "use_well_known_port": "yes",
                                    "use_ssl": "yes",
                                    "transfer_preset": ""
                                }
                            }
                        }
                    }
                },
                "content_uri": "",
                "session_operation_auth": {
                    "session_operation_auth_by_signature": {
                        "token": d["token"],
                        "signature": d["signature"]
                    }
                },
                "content_auth": {
                    "auth_type": "ht2",
                    "content_key_timeout": d["content_key_timeout"],
                    "service_id": "nicovideo",
                    "service_user_id": d["service_user_id"]
                },
                "client_info": {
                    "player_id": d["player_id"]
                },
                "priority": d["priority"]
            }
        }
        session_url = "https://api.dmc.nico/api/sessions?_format=json"
        response = await session.post(session_url, json=payload)
        response.raise_for_status()
        data = await response.json()
        
        return data["data"]["session"]["content_uri"]

async def main():
    nv = NiconicoVideo("https://www.nicovideo.jp/watch/sm32038706")

    async with aiohttp.ClientSession() as session:
        url = await nv.getDownloadUrl(session)
    print(url)
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())