from abc import ABC, abstractmethod
from typing import BinaryIO

class Storage(ABC):
    @abstractmethod
    async def save(self, file_data: BinaryIO, object_name: str, content_type: str) -> str:
        """Save file and return object identifier (e.g., object name)."""
        pass

    @abstractmethod
    async def get(self, object_name: str):
        """Retrieve file as a stream."""
        pass

    @abstractmethod
    async def delete(self, object_name: str):
        """Delete file."""
        pass