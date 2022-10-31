import decimal


def decimalPart_to_hex(value: decimal.Decimal, length: int) -> str:
    '''
    Convert a fractional part to a binary representation
    limited by the number of bits who wants to be
    representated.

    NOTE: Recomended use decimal.Decimal type to ensure Decimal
    numbers can be represented exactly. float numbers do not
    have exact representations in binary floating point.

    Explanation:

    Rational number structure.

            whole part
            ┌───────┐
            │1 2 3 4│.│5 6 7 8│
                      └───────┘
                    fractional part
    
    The convertion follows the rules below:

    1. Take the fraction part
    2. Multiply it by 16 , substract the whole part
    3. If the whole part is between 10-15 map it with A-F
       The substract whole part its now part of the hex value
    4. Go to number step 1. until completing the amount of hex values

    Example: Get the first 3 bytes of 0.41421 base 10 into base 16

    0.41421 x 16 =  6.62736 ->  6 -> 6
    0.62736 x 16 = 10.03776 -> 10 -> 6a
    0.03776 x 16 =  0.60416 ->  0 -> 6a0
    0.60416 x 16 =  9.66656 ->  9 -> 6a09
    0.66656 x 16 = 10.66496 -> 10 -> 6a09a
    0.66496 x 16 = 10.63936 -> 10 -> 6a09aa

    '''
def decimalPart_to_hex(value: decimal.Decimal, length: int) -> str:
    new = value*16
    whole = int(new)
    fractional_part = new - whole
    length += -1
    if length >= 0:
        return hex(whole)[2:] + decimalPart_to_hex(fractional_part, length)
    else:
        return ''


def decimalPart_to_binary(value: decimal.Decimal, length: int) -> str:
    '''
    Convert a fractional part to a binary representation
    limited by the number of bits who wants to be
    representated.

    NOTE: Recomended use decimal.Decimal type to ensure Decimal
    numbers can be represented exactly. float numbers do not
    have exact representations in binary floating point.

    Explanation:

    Rational number structure.

            whole part
            ┌───────┐
            │1 2 3 4│.│5 6 7 8│
                      └───────┘
                    fractional part
    
    The convertion follows the rules below:

    1. Take the fraction part
    2. Multiply it by 2 , substract the whole part
       The substract whole part its now part of the binary value
    3. Go to number step 1. until completing the amount of bits

    Example: Get the first 5 bits of 0.41421 base 10 into base 16

    0.41421 x 2 = 0.82842 -> 0
    0.82842 x 2 = 1.65684 -> 01
    0.65684 x 2 = 1.31368 -> 011
    0.31368 x 2 = 0.62736 -> 0110
    0.62736 x 2 = 1.25472 -> 01101
    0.62736 x 2 = 1.25472 -> 01101
    '''

    new = value*2
    whole = int(new)
    fractional_part = new - whole
    length += -1
    if length >= 0:
        return str(whole) + decimalPart_to_binary(fractional_part, length)
    else:
        return ''



