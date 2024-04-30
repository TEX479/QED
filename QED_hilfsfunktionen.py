
def IntToBit(x:int, length:int=8) -> str:
    return "0"*((length - (x.bit_length() % length)) * int(x.bit_length() % length != 0)) + bin(x)[2:]

def BitToInt(s:str, anz_bit= 8) -> list[int]:
    if len(s)%anz_bit != 0: s = s + ("0" * (anz_bit - (len(s) % anz_bit)))
    return [int(s[i:i+anz_bit], 2) for i in range(0, len(s), anz_bit)]

def int2anybase(input_number:int, base:int) -> list[int]:
    if input_number == 0:
        return [0]
    
    output_number = []
    while input_number > 0:
        output_number.append(input_number%base)
        input_number = input_number//base
    output_number.reverse()

    return output_number

def int2anybase2(input_number:int, base:float) -> list[float]:
    if input_number == 0:
        return [0]

    output_number = []
    while input_number > 0:
        output_number.append(((input_number*10)%int(base*10))/10)
        input_number = (input_number*10)//int(base*10)
    output_number.reverse()

    return output_number

def anybase2anybase(input_number:list, input_base:int, output_base:int) -> list[int]:
    processing_nuber = 0
    for i in range(len(input_number)):
        processing_nuber += input_number[len(input_number)-i-1]*input_base**i

    if processing_nuber == 0:
        return [0]

    output_number = []
    while processing_nuber > 0:
        output_number.append(processing_nuber%output_base)
        processing_nuber = processing_nuber//output_base
    output_number.reverse()
    
    return output_number
