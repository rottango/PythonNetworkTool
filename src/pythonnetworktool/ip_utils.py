def parse_ip_addr(ip_addr):
    str_octets=ip_addr.split('.',4)
    int_octets = []
    
    if len(str_octets) != 4:
        print("ip_addr doesnt have 4 bytes")
        return False, None
    
    for byte in str_octets:
        if not byte.isdigit():
            print("ip_addr is not numeric")
            return False, None
        int_octets.append(int(byte))

    if not _verify_ip_addr(int_octets=int_octets):
        print("one of the 4 bytes of the IPv4 ip_addr is bigger than 255 or smaller than 0")
        return False, None
    
    print("ip_addr split into int_octets: ", end=" ")
    for byte in int_octets:
        print(byte, end=" ")
    print()
    
    return True, int_octets

def is_in_subnet(ip_addr, subnet):
    valid_ip_addr, ip_addr_octets = parse_ip_addr(ip_addr=ip_addr)
    if not valid_ip_addr:
        return False
    
    valid_subnet, subnet = parse_ip_addr(ip_addr=subnet)
    if not valid_subnet:
        return False

    host_identifier=[0,0,0,0]
    network_prefix=[0,0,0,0]

    #network_prefix
    for th_octet in range(len(ip_addr_octets)):
        network_prefix[th_octet]=ip_addr_octets[th_octet] & subnet[th_octet] 
    
    
    #host_identifier
    for th_octet in range(len(ip_addr_octets)):
        host_identifier[th_octet]=ip_addr_octets[th_octet] & ~subnet[th_octet] 
        

    host_identifier_str=_connect_octet_into_one_str(host_identifier)
    network_prefix_str=_connect_octet_into_one_str(network_prefix)
    print(host_identifier_str)
    print(network_prefix_str)

def _verify_ip_addr(int_octets):
    for byte in int_octets:
        if byte > 255 or byte < 0:
             return False
    return True

def _connect_octet_into_one_str(octet):
    
    addr=""
    for byte in octet:
        addr+=str(byte)+"."
    
    return addr[:-1]

if __name__ == "__main__":
    is_in_subnet(ip_addr="192.0.2.130", subnet="255.255.255.192")