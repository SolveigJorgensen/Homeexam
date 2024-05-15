# The following code is taken from my personal obligs and is used to
# input for portnumber and ip adress and handels exceptions
import argparse
import time


def valid_ip(ip):
    try:
        list = ip.split(".",
                        3)  # This code splits the string into a list. The seperator = . and the maksimal split is set to 3.

        for value in list:
            number = int(value)
            if not 0 <= number <= 255:  # Checks if the number is in the range [0, 255] if not raise exception
                raise ValueError()

    except ValueError:
        raise argparse.ArgumentTypeError('The ip adress must be in the notation format e.g. 10.0.0.2')

    return ip


# This function checks if the port nr is valid. It takes in the portnumber and returns it if it is in the range [1024, 65535]
def valid_port(port):
    try:
        portnr = int(port)
        if not 1024 <= portnr <= 65535:
            raise ValueError()

    except ValueError:
        raise argparse.ArgumentTypeError('The portnumber must be a integer and in the range 1024 - 65535')

    return portnr


def valid_window(windowsize):
    try:
        windowsize = int(windowsize)
        if not 1 <= windowsize <= 10:
            raise ValueError

    except ValueError:
        raise argparse.ArgumentTypeError('The windowsize must be a integer and in the range 1 - 10')

    return windowsize


def valid_discard_packet(discard_packet):
    try:
        discard_packet = int(discard_packet)
        if discard_packet < 1:
            raise ValueError

    except ValueError:
        raise argparse.ArgumentTypeError('Packet to be discard must be a integer bigger than 0')

    return discard_packet

def valid_filename(filename):

    try:
        if not filename.endswith('.jpg'):
            raise ValueError

    except ValueError:
        raise argparse.ArgumentTypeError('File must be a jpg file.')

    return filename