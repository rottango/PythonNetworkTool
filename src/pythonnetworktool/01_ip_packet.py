# create an ip packet

from scapy.all import IP

ip_packet = IP(dst="192.168.1.1")