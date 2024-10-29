"""
Checksum
"""

class Checksum:
    """Calculate Checksum"""
    
    def checksum(self, data):
        """
        Calculate the checksum of the data and returns it
        """
        data = data.encode('utf-8')

        checksum = 0
        for byte in data:
            checkum += byte
            
        return checksum % 256