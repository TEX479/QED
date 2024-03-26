
def IntToBit(x:int, lenght = 8):
        return f"{x:0{lenght}b}"

def int2anybase(number:int, base:int):
    if number != 0:
        number_ = []
        while number > 0:
            number_.append(number%base)
            number = number//base
        number_.reverse()
    else:
        number_ = [0]
    return number_

def int2anybase2(number:int, base:float):
    if number != 0:
        number_ = []
        #l_komma = 10**len((str(base).split("."))[1])
        while number > 0:
            number_.append(((number*10)%int(base*10))/10)
            number = (number*10)//int(base*10)
        number_.reverse()
    else:
        number_ = [0]
    return number_

def anybase2anybase(number_:list, input_base:int, output_base:int):
    number = 0
    for i in range(len(number_)):
        number += number_[len(number_)-i-1]*input_base**i

    if number != 0:
        output_number = []
        while number > 0:
            output_number.append(number%output_base)
            number = number//output_base

        output_number.reverse()
    else:
        output_number = [0]
    return output_number
