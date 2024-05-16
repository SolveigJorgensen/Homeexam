# -------------- Input validation ------------ #

#The following code contains input validation functions and is mostly taken from my previous assignments/obligs.

import argparse

# Description:
#   Input validation for ip andress, checks if in in the format X.X.X.X,
#   and that the values are between 0 and 255. If not it raises exception.
# Parameters:
#   ip: Ip adress set by user.
# Returns:
#   A string with IP adress
def check_ip(ip):
    try:
        list = ip.split(".", 3)         # Splits the string into a list. The seperator = . and the maxsimal split is set to 3.

        for value in list:
            number = int(value)
            if not 0 <= number <= 255:  # Checks if the number is in the range [0, 255] if not raise exception
                raise ValueError()

    except ValueError:
        raise argparse.ArgumentTypeError('The ip adress must be in the notation format e.g. 10.0.0.2')

    return ip

# Description:
#   Input validation for port number, checks if input is an integer between 1024 and 65535
#   If not it raises exception.
# Parameters:
#   port: Port number set by user.
# Returns:
#   A integer with port number
def check_port(port):
    try:
        portnr = int(port)
        if not 1024 <= portnr <= 65535:
            raise ValueError()

    except ValueError:
        raise argparse.ArgumentTypeError('The portnumber must be a integer and in the range 1024 - 65535')

    return portnr

# Description:
#   Input validation for windowsize, checks if input is an integer between 1 and 10
#   If not it raises exception.
# Parameters:
#   windowsize: Windowsize set by user.
# Returns:
#   A integer with windowsize
def check_window(windowsize):
    try:
        windowsize = int(windowsize)
        if not 1 <= windowsize <= 10:
            raise ValueError

    except ValueError:
        raise argparse.ArgumentTypeError('The windowsize must be a integer and in the range 1 - 10')

    return windowsize

# Description:
#   Input validation for discard packet, checks if input is an integer and equals 1 og bigger.
#   If not it raises exception.
# Parameters:
#   discard packet: Packet to be discarded set by user.
# Returns:
#   A integer with packet to be discarded.
def check_discard_packet(discard_packet):
    try:
        discard_packet = int(discard_packet)
        if discard_packet < 1:
            raise ValueError

    except ValueError:
        raise argparse.ArgumentTypeError('Packet to be discard must be a integer bigger than 0')

    return discard_packet

# Description:
#   Input validation for filename, checks if the file is a jpg file.
#   If not it raises exception.
# Parameters:
#   filename : Filename set by user, either file to send og filename the recived file should have on the server side.
# Returns:
#   String with filename
def check_filename(filename):
    try:
        if not filename.endswith('.jpg'):
            raise ValueError

    except ValueError:
        raise argparse.ArgumentTypeError('File must be a jpg file.')

    return filename