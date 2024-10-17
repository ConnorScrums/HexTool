"""Interprets an item as a 64-bit hash."""

from hash import Hash


class Hash64Bit(Hash):
    """Concrete Hash Class which interprets an input as a 64-bit hash."""

    def to_hash_string(self) -> str:
        """Converts item to hash string.

        Returns:
            Hash String
        """
        return f"{self.fnv1a_64bit_hash():16x}"

    def fnv1a_64bit_hash(self):
        """Concrete Hash Class which interprets an input as a 64-bit hash.

        Returns:
            Hash String
        """
        # Constants for FNV-1a 64-bit
        fnv_prime = 0x100000001B3
        fnv_offset_basis = 0xCBF29CE484222325

        # Start with the offset basis
        hash_value = fnv_offset_basis

        # Process each byte in the input string
        for char in str(self.item):
            # XOR the byte with the hash value
            hash_value ^= ord(char)
            # Multiply by the FNV prime, using modulo to keep it 64-bit
            hash_value = (hash_value * fnv_prime) & 0xFFFFFFFFFFFFFFFF

        return hash_value
