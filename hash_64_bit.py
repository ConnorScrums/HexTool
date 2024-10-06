from hash import Hash

class Hash64Bit(Hash):
    def __init__(self, item: any) -> None:
        super().__init__(item)

    def __repr__(self) -> str:
        return f"{self.fnv1a_64bit_hash()}"
    
    def fnv1a_64bit_hash(self):
        # Constants for FNV-1a 64-bit
        fnv_prime = 0x100000001b3
        fnv_offset_basis = 0xcbf29ce484222325

        # Start with the offset basis
        hash_value = fnv_offset_basis

        # Process each byte in the input string
        for char in str(self.item):
            # XOR the byte with the hash value
            hash_value ^= ord(char)
            # Multiply by the FNV prime, using modulo to keep it 64-bit
            hash_value = (hash_value * fnv_prime) & 0xFFFFFFFFFFFFFFFF

        return hash_value