def parse_ip_addr(ip_addr):
    str_octets = ip_addr.split(".", 4)
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
        print(
            "one of the 4 bytes of the IPv4 ip_addr is bigger than 255 or smaller than 0"
        )
        return False, None

    print("ip_addr split into int_octets: ", end=" ")
    for byte in int_octets:
        print(byte, end=" ")
    print()

    return True, int_octets


def host_identfier_and_network_prefix(ip_addr, subnet):
    valid_ip_addr, parsed_ip_addr = parse_ip_addr(ip_addr=ip_addr)
    if not valid_ip_addr:
        return False, None, None

    valid_subnet, parsed_subnet = parse_ip_addr(ip_addr=subnet)
    if not valid_subnet:
        return False, None, None

    parsed_host_identifier = [0, 0, 0, 0]
    parsed_network_prefix = [0, 0, 0, 0]

    # parsed_network_prefix
    for th_octet in range(len(parsed_ip_addr)):
        parsed_network_prefix[th_octet] = (
            parsed_ip_addr[th_octet] & parsed_subnet[th_octet]
        )

    # parsed_host_identifier
    for th_octet in range(len(parsed_ip_addr)):
        parsed_host_identifier[th_octet] = (
            parsed_ip_addr[th_octet] & ~parsed_subnet[th_octet]
        )

    return True, parsed_host_identifier, parsed_network_prefix


def is_ip_addr_in_network(ip_addr, target_network, target_network_mask):

    valid_ip_addr, parsed_ip_addr = parse_ip_addr(ip_addr=ip_addr)
    if not valid_ip_addr:
        return False

    valid_target_network, parsed_target_network = parse_ip_addr(ip_addr=target_network)
    if not valid_target_network:
        return False

    valid_target_network_mask, parsed_target_network_mask = parse_ip_addr(
        ip_addr=target_network_mask
    )
    if not valid_target_network_mask:
        return False

    for th_octet in range(len(parsed_ip_addr)):
        if not (
            (parsed_ip_addr[th_octet] & parsed_target_network_mask[th_octet])
            == parsed_target_network[th_octet]
        ):
            print(
                "The ip_addr "
                + _connect_octet_into_one_str(parsed_ip_addr)
                + "is not in network "
                + _connect_octet_into_one_str(parsed_target_network)
            )
            return False

    print(
        "The ip_addr "
        + _connect_octet_into_one_str(parsed_ip_addr)
        + " is in network "
        + _connect_octet_into_one_str(parsed_target_network)
    )

    return True


def _verify_ip_addr(int_octets):
    for byte in int_octets:
        if byte > 255 or byte < 0:
            return False
    return True


def _short_mask_to_parsed_mask(short_mask):
    if len(short_mask) not in range(2, 4):
        print("Wrong short_mask format provided, expected /xx or /x")
        return False

    if short_mask[0] != "/":
        print("Wrong short_mask format provided, expected / at the start")
        return False

    number_of_ones_in_mask = short_mask[1:]

    if not number_of_ones_in_mask.isdigit():
        print("Wrong short_mask format provided, only digits allowed")
        return False

    number_of_ones_in_mask = int(number_of_ones_in_mask)

    if number_of_ones_in_mask not in range(0, 32 + 1):
        print("Wrong value of mask, not in range <0;32>")
        return False

    parsed_mask = [0, 0, 0, 0]

    number_of_full_bytes = number_of_ones_in_mask // 8
    remainder_bits = number_of_ones_in_mask % 8

    for full_byte in range(0, number_of_full_bytes):
        parsed_mask[full_byte] = 255

    if number_of_full_bytes < 4 and remainder_bits != 0:
        for x in range(0, remainder_bits):
            parsed_mask[number_of_full_bytes] += 2 ** (7 - x)

    return parsed_mask


def _connect_octet_into_one_str(octet):

    addr = ""
    for byte in octet:
        addr += str(byte) + "."

    return addr[:-1]


if __name__ == "__main__":
    is_ip_addr_in_network(
        ip_addr="192.0.2.127",
        target_network="192.0.2.128",
        target_network_mask="255.255.255.192",
    )

    for mask in [
        "/0",
        "/1",
        "/7",
        "/8",
        "/9",
        "/16",
        "/24",
        "/25",
        "/26",
        "/31",
        "/32",
    ]:
        print(mask, _connect_octet_into_one_str(_short_mask_to_parsed_mask(mask)))
