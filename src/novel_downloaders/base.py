from abc import ABC, abstractmethod
from typing import List, Dict, Union

class NovelDownloaderBase(ABC):
    @abstractmethod
    def download_novel(self, novel_id: Union[str, int]) -> bool:
        """
        Download a novel by its ID
        Returns True if successful, False otherwise
        """
        pass

    @abstractmethod
    def search_novel(self, keyword: str) -> List[Dict]:
        """
        Search for novels by keyword
        Returns list of novel info dictionaries
        """
        pass

    @abstractmethod
    def update_all_novels(self):
        """
        Update all novels in records
        """
        pass
