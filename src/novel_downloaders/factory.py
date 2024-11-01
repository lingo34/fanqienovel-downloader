from typing import Type
from .base import NovelDownloaderBase
from .fanqie import FanqieNovelDownloader

class NovelDownloaderFactory:
    @staticmethod
    def create_downloader(downloader_type: str) -> Type[NovelDownloaderBase]:
        if downloader_type == 'fanqie':
            return FanqieNovelDownloader
        else:
            raise ValueError(f"Unknown downloader type: {downloader_type}")
