import logging
from pathlib import Path
import json

# Get the logger we already configured by its name
logger = logging.getLogger("SQLValidator")


class FileHandler:
    """A utility class to manage different file input types."""

    @staticmethod
    def read(source: str):
        path = Path(source)

        if path.is_file():
            logger.info(f"Valid File Found : {path}")
            return FileHandler._handle_file(path)
        
        logger.info(f"Valid String Found : {source}")
        return source   # its just a raw string
    
    @staticmethod
    def _handle_file(path: Path):
        """Internal helper method to route file extensions."""
        if path.suffix == ".txt":
            return path.read_text()
        elif path.suffix == '.json':
            return FileHandler._parse_json(path)
        else:
            logger.warning(f"Unsupported file type : {path.suffix}")
            return None
        
    @staticmethod
    def _parse_json(path: Path):
        try:
            with open(path, 'r') as f:
                data = json.load(f)

                return data.get("query", "")
        except Exception as e:
            logger.error(f"Failed to parse JSON : {e}")
            return None
