from zlib import crc32
from typing import IO

class Checksum:
    """
    Checksum to verify that the file is not tampered with
    """
    def crc32_checksum_file(self, file_input: IO) -> int:
        """
        Args:
            file_input: File uploaded to application taken as input
        """
        crc32_value = 0
    
        with open(file_input, 'rb') as f:
            while chunk := f.read(1024):  # Read in 1024-byte chunks
                crc32_value = crc32(chunk, crc32_value)

        return crc32_value
