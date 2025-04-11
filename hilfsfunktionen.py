
def IntToBit(x:int, lenght:int = 8) -> str:
    return f"{x:0{lenght}b}"

def BitToInt(s:str, anz_bit:int= 8) -> list[int]:
    """
    returns list[int] with int.len() == "anz_bit"
    """
    r: list[int]= []
    for i in range(len(s)//anz_bit):
        r.append(int(s[i*anz_bit:(i+1)*anz_bit], 2))
    if len(s)%anz_bit != 0:
        r.append(int(s[(len(s)//anz_bit)*anz_bit:], 2))
    return r

def int2anybase(number:int, base:int) -> list[int]:
    if number != 0:
        number_: list[int] = []
        while number > 0:
            number_.append(number%base)
            number = number//base
        number_.reverse()
    else:
        number_ = [0]
    return number_

def int2anybase2(number:int, base:float) -> list[float]:
    if number != 0:
        number_: list[float] = []
        #l_komma = 10**len((str(base).split("."))[1])
        while number > 0:
            number_.append(((number*10)%int(base*10))/10)
            number = (number*10)//int(base*10)
        number_.reverse()
    else:
        number_ = [0]
    return number_

def anybase2anybase(number_:list[int], input_base:int, output_base:int) -> list[int]:
    number = 0
    for i in range(len(number_)):
        number += number_[len(number_)-i-1]*input_base**i

    if number != 0:
        output_number: list[int] = []
        while number > 0:
            output_number.append(number%output_base)
            number = number//output_base

        output_number.reverse()
    else:
        output_number = [0]
    return output_number
