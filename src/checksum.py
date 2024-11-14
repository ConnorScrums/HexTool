from zlib import crc32
from typing import IO

class Checksum:
    """
    Calculate the checksum of a file to verify integrity
    """
    def calculate_checksum(self, file_input: IO) -> int:
        """
        Args:
            file_input: File uploaded to application taken as input
        """
        crc32_value = 0
    
        with open(file_input, 'rb') as f:
            while chunk := f.read(1024):  # Read in 1024-byte chunks
                crc32_value = crc32(chunk, crc32_value)

        return crc32_value
