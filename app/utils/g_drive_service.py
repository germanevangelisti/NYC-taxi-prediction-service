import os
from cachetools import Cache
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

current_directory = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(current_directory, 'credentials.json')

class MemoryCache(Cache):
    def __init__(self, maxsize):
        super().__init__(maxsize)

    def get(self, url):
        return self._CACHE.get(url)

    def set(self, url, content):
        self._CACHE[url] = content

class GoogleDriveService:
    def __init__(self):
        self._SCOPES=['https://www.googleapis.com/auth/drive']

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

    def build(self):
        creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"), self._SCOPES)
        service = build('drive', 'v3', cache=MemoryCache(maxsize=100), credentials=creds)

        return service