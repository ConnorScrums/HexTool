"""
Folding hash implementation, breaks up key value into 
segments that are added to form a hash value
"""
from hash import Hash
from hash_64_bit import Hash64Bit
from hasher import Hasher

class FoldingMethodHasher(Hasher):
    """
    Python implementation of the folding hash
    """
    def __call__(self, raw_bytes: bytes) -> Hash:
        """Allows this class to be called as if it were a function."""
        return self.hash(raw_bytes)

    def hash(self, raw_bytes: bytes) -> Hash:
        # Assuming we want to fold the bytes into 8-byte chunks
        chunk_size = 8
        num_chunks = (len(raw_bytes) + chunk_size - 1) // chunk_size
        # Initialize a total hash value
        total_hash = 0
        # Process each chunk
        for i in range(num_chunks):
            chunk = raw_bytes[i * chunk_size: (i + 1) * chunk_size]
            # Convert the chunk to an integer
            chunk_value = int.from_bytes(chunk, byteorder='big')
            total_hash += chunk_value
        # Create a Hash64Bit instance with the final folded value
        return Hash64Bit(total_hash)
    