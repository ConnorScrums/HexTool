from hash import Hash
from hash_64_bit import Hash64Bit
from hasher import Hasher

class MidSquareHasher(Hasher):
    def hash(self, bytes: bytes) -> Hash:
        # Convert the input bytes to an integer
        initial_value = int.from_bytes(bytes, byteorder='big')

        # Square the integer
        squared_value = initial_value ** 2
        
        # Convert the squared value to a string to extract digits
        squared_str = str(squared_value)
        
        # Use the middle portion of the squared value
        mid_length = len(squared_str)
        if mid_length <= 4:
            # If the squared value has 4 digits or less, use it directly
            hash_value = squared_value
        else:
            mid_index = mid_length // 2
            # Extract the middle four digits
            start = max(0, mid_index - 2)
            end = min(mid_length, mid_index + 2)
            hash_value = int(squared_str[start:end])

        # Create a Hash64Bit instance with the final hash value
        return Hash64Bit(hash_value)
