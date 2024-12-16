import socket

def ip_to_code():
    ip_address = socket.gethostbyname(socket.gethostname())
    ip_address_list = ip_address.split('.')

    code = ''
    for n in ip_address_list:
        nhex = '{:x}'.format(int(n))
        if len(nhex) < 2:
            nhex = '0' + nhex
        code += nhex

    code = code.upper()
    return ip_address, code

# CONVERTS IP ADDRESS TO CODE
ip_address, code = ip_to_code()
print(code)

print("IP Address:", ip_address)
print("Hex Code:", code)




# CONVERTS CODE TO IP ADDRESS
def code_to_ip(hex_code):
    if len(hex_code) != 8:
        raise ValueError("Invalid hex code length. Must be 8 characters.")

    ip_parts = []
    for i in range(0, len(hex_code), 2):
        part = hex_code[i:i+2]
        ip_parts.append(str(int(part, 16)))

    return '.'.join(ip_parts)

# Example usage
converted_ip = code_to_ip(code)
print("Converted IP Address:", converted_ip)