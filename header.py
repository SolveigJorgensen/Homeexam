'''This code is taken from safiqul and creates a header for the packets'''

'''
    #Utility functions: 1) to create a packet of 1472 bytes with header (12 bytes) (sequence number, acknowledgement number,
    #flags and receiver window) and applicaton data (1460 bytes), and 2) to parse
    # the extracted header from the application data. 

'''

from struct import *
import time

# I integer (unsigned long) = 4bytes and H (unsigned short integer 2 bytes)
# see the struct official page for more info

header_format = '!HHH'

# print the header size: total = 6
print(f'size of the header = {calcsize(header_format)}')


def create_packet(seq, ack, flags, data):
    # Creates a packet with sequence number, acknowledgment number,
    # flags and data.
    header = pack(header_format, seq, ack, flags)

    # once we create a header, we add the application data to create a packet
    # of 994 bytes
    packet = header + data
    return packet


def parse_header(header):
    # taks a header of 6 bytes as an argument,
    # unpacks the value based on the specified header_format
    # and return a tuple with the values
    header_from_msg = unpack(header_format, header)
    # parse_flags(flags)
    return header_from_msg


def parse_flags(flags):
    # we only parse the first 3 fields because we're not
    # using rst in our implementation
    syn = bool(flags & (1 << 3))
    ack = bool(flags & (1 << 2))
    fin = bool(flags & (1 << 1))
    return syn, ack, fin

#This function takes a packet in, and returns the flags.
def parse_packet(packet_recived):
    header_recived = packet_recived[:6]
    seq, ack, flags = parse_header((header_recived))
    syn, ack, fin = parse_flags(flags)
    return (syn, ack, fin)








