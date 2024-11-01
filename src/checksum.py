"""
Checksum
"""

import zlib

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
    
    def find_checksum_sender(sent_message):

        k = 8 # number of bits

        c1 = sent_message[0:k]
        c2 = sent_message[k:2*k]
        c3 = sent_message[2*k:3*k]
        c4 = sent_message[3*k:4*k]

        sum_of_packets = bin(int(c1, 2) + int(c2, 2) + int(c3, 2) + int(c4, 2))[2:]

        if(len(sum_of_packets) > k):
            x = len(sum_of_packets) - k
            sum_of_packets = bin(int(sum_of_packets[0:x], 2)+int(sum_of_packets[x:], 2))[2:]        
        if(len(sum_of_packets) < k):
            sum_of_packets = '0'*(k-len(sum_of_packets))+sum_of_packets

        checksum = ''
        for i in sum_of_packets:
            if(i == '1'):
                checksum += '0'
            else:
                checksum += '1'
        return checksum
    
    def find_checksum_receiver(received_message):

        k = 8

        # Dividing sent message in packets of k bits.
        c1 = received_message[0:k]
        c2 = received_message[k:2*k]
        c3 = received_message[2*k:3*k]
        c4 = received_message[3*k:4*k]
    
        # Calculating the binary sum of packets + checksum
        ReceiverSum = bin(int(c1, 2)+int(c2, 2)+int(Checksum, 2) +
                          int(c3, 2)+int(c4, 2)+int(Checksum, 2))[2:]
    
        # Adding the overflow bits
        if(len(ReceiverSum) > k):
            x = len(ReceiverSum)-k
            ReceiverSum = bin(int(ReceiverSum[0:x], 2)+int(ReceiverSum[x:], 2))[2:]
    
        # Calculating the complement of sum
        ReceiverChecksum = ''
        for i in ReceiverSum:
            if(i == '1'):
                ReceiverChecksum += '0'
            else:
                ReceiverChecksum += '1'
        return ReceiverChecksum