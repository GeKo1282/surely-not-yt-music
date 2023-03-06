import ytmusicapi
import orjson as json
import asyncio

class YTMFetcher():
    def __init__(self, login, password) -> None:
        self.api = ytmusicapi.YTMusic()
    
