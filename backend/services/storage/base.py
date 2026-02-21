from abc import ABC, abstractmethod
from typing import BinaryIO, Optional

class Storage(ABC):
    @abstractmethod
    async def save(self, file_data: BinaryIO, object_name: str, content_type: str, size: Optional[int] = None) -> str:
        """Save file and return object identifier. If size is known, it can be used."""
        pass

    @abstractmethod
    async def get(self, object_name: str):
        """Retrieve file as a stream."""
        pass

    @abstractmethod
    async def delete(self, object_name: str):
        """Delete file."""
        pass