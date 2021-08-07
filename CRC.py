from helper import binary, str2bin, bin2str

# Reference for _CRC function
#       _____q_____
#    abc|d1
#       |d2
#       |-----
#       | d1
#       | d2
#       | ----
#       |  d1
#       |  d2
#       |  ---
#       |  remainder

# d2 can be either 0s or the divisor


def _CRC(binaryData: str, divisor: str, *, verify: bool):
    '''
    If verify is False, returns the CRC using the provided divisor
    If verify is True, returns True if data is not corrupted
    '''

    # Sender calculates the remainder on data using the divisor and appends remainder to the data.
    # Receiver calculates on data received by sender remainder using the divisor if its 0, then the data is not corrupt

    if isinstance(divisor, int):
        divisor = binary(divisor)

    # Remove any leading 0s from the binaryData and divisor
    binaryData = binaryData.lstrip('0')
    divisor = divisor.lstrip('0')

    # Indicator of which digit to drop
    i = len(divisor) - 1

    if not verify:
        # Add len(divisor) - 1 bits with value 0 to the data (Redundant Bits)
        binaryData = binaryData + ''.join(['0' for _ in range(len(divisor) - 1)])

    # Find the initial dividend
    d1 = binaryData[0 : len(divisor) - 1]

    while i < len(binaryData):
        # Drop the digit
        d1 += binaryData[i]
        d2 = '0'*len(divisor) if d1[0] == '0' else divisor

        # Perform XOR between d1 and d2
        d1 = ''.join(['1' if bit0 != bit1 else '0' for bit0, bit1 in list(zip(d1, d2))[1:]]) # Skip leading bit
        i += 1

    # Add the digits that weren't dropped
    remainder: str = d1 + binaryData[i: ]
 
    # NOTE: Don't remove any leading 0s from remainder

    if verify:
        # The remainder is 0, if the data is not corrupted
        return True if int(remainder) == 0 else False
        # return "Data is intact!" if remainder == '' else "Data got corrupted!"

    return remainder

def compute_CRC(binaryData: str, divisor: str) -> str:
    '''
    Return the CRC for the given data
    '''
    return _CRC(binaryData, divisor, verify=False)


def verify_CRC(binaryData: str, divisor: str) -> bool:
    '''
    Return True if data is not corrupted
    '''
    return _CRC(binaryData, divisor, verify=True)

def corrupt_message(binaryString: str) -> str:
    '''
    This might flip few of the bits of the data
    '''
    from random import random, choice
    binaryString = list(binaryString)
    for i in range(len(binaryString)):
        corruptibility_factor = 0.01
        if random() < corruptibility_factor:
            binaryString[i] = choice(['1', '0'])                              # Might flip might not
            # binaryString[i] = '0' if binaryString[i] == '1' else '1'          # Flip
            # binaryString[i] = str(int(binaryString[i]) + 1 % 2)               # Flip
    return ''.join(binaryString)

# def CRC_32(binaryData: str):
#     '''
#     Compute CRC-32 in hexadecimal
#     '''
#     print('Binary Data:', binaryData)
#     integer_CRC = int(compute_CRC(binaryData, binary((0x04C11DB7))), 2)
#     print("CRC Value\n\t=>Int:", integer_CRC, "\n\t=>Hex:", hex(integer_CRC))
#     return integer_CRC

def main():
    # Sender wants to send this message
    message_text = "Hello World!"
    message = str2bin(message_text)
    divisor = '1011'

    # Compute the message's CRC using the given divisor
    print("-----------------------------------------------------------")
    print('Divisor used for computing CRC:', divisor)
    print('Message being sent:', message_text)
    print('Message in Binary:', message)
    print('CRC Value:', compute_CRC(message, divisor))

    # Add CRC to the message
    message = message + compute_CRC(message, divisor) 

    # Send message
    print("-----------------------------------------------------------")
    print('Transmitting message........')
    print("-----------------------------------------------------------")

    # Message `might` get corrupted due to transmission errors
    transmitted_message = corrupt_message(message)

    # Receiver receives and checks whether data got corrupted
    received_message = transmitted_message
    # Removing the bits used by CRC
    actual_received_message = transmitted_message[:len(transmitted_message)-len(divisor)+1]

    print('Receiver received the message:', bin2str(actual_received_message))
    print('Message in Binary:', actual_received_message)
    print('Data Corrupted:', not verify_CRC(received_message, divisor))
    print("-----------------------------------------------------------")

if __name__ == "__main__":
    main()
    # CRC_32(str2bin('a'))
    # print('CRC:',compute_CRC('1101101', '10011'))
    # print('CRC:',compute_CRC(str2bin('m'), '100110000010001110110110111'))
    # compute_CRC(str2bin('m'), '10011')