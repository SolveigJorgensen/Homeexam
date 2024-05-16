# ------------ Header  --------- #

# The following code include the functions regarding header and packets in the DRTP-Application and is copyed from code provided
# by Safiquel Islam on https://github.com/safiqul/2410/blob/main/header/header.py, some code is modified.

from struct import *

# This is the format of the header. Containing 6 bytes, split into 3 parst of 2 bytes. H stands for unsigned short integer.
# Values for the header is assigned when create_packet() function is used.
header_format = '!HHH'

# Description:
#   Creates a packet with sequence number, acknowledgment number,
#   flags and data. The header include the seq number, ack number and flags.
#   The application data is then added to the header.
# Parameters:
#   seq: Sequence number of the packet
#   ack: Acknoledgment number,  it is used to send an acknowledgment back to the client with the same number as the received sequence number.
#   flags: contain bits for S = SYN flag, A= ACK flag, F=FIN flag, R= Reset Flag used in a threeway handshake.
#   data: Contains data that gets attached to the header.
# Returns:
#   A packet with a header and data.
def create_packet(seq, ack, flags, data):
    header = pack(header_format, seq, ack, flags)
    packet = header + data
    return packet

# Description:
#   Takes a header of 6 bytes as argument,unpacks the value based on the specified header_format
#   and return a tuple with the values
# Parameters:
#   header: First 6 bytes in a packet
# Returns:
#   A tuple of the header values (seq, ack, flags)
def parse_header(header):
    header_from_msg = unpack(header_format, header)
    return header_from_msg


# Description:
#   Parse the first 3 fields in a flag. We dont use Reset flag.
# Parameters:
#   flags: contain bits for S = SYN flag, A= ACK flag, F=FIN flag, R= Reset Flag used in a threeway handshake.
# Returns:
#   A tuple with boolean values of the flags values (syn, ack, fin) where true means that the flag is set.
def parse_flags(flags):
    syn = bool(flags & (1 << 3))
    ack = bool(flags & (1 << 2))
    fin = bool(flags & (1 << 1))
    return syn, ack, fin

# Description:
#   Parse a packet, takes a packet as argument, reads and parses the header, and then parse the flags.
# Parameters:
#   seq: Sequence number of the packet
#   ack: Acknoledgment number, it is used to send an acknowledgment back to the client with the same number as the received sequence number.
#   flags: contain bits for S = SYN flag, A= ACK flag, F=FIN flag, R= Reset Flag used in a threeway handshake.
# Returns:
#   A tuple with boolean values of the flags values (syn, ack, fin) where true means that the flag is set.
def parse_packet(packet_recived):
    header_recived = packet_recived[:6]
    seq, ack, flags = parse_header((header_recived))
    syn, ack, fin = parse_flags(flags)
    return (syn, ack, fin)








