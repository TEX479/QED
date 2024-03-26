import math
from random import randint
import multiprocessing
import time

def StrToBit(x:str|list, lenght = 8):
        text = ""
        lengths = []
        for i in x:
            lengths.append(math.ceil((len(bin(ord(i)))-2)/lenght)*lenght)
            text += "0"*((math.ceil((len(bin(ord(i)))-2)/lenght)*lenght+2)-len(bin(ord(i)))) + bin(ord(i))[2:]
        return text, lengths

def BitToStr(s:str, anz_bit:int):
        r= ""
        for i in range(len(s)//anz_bit):
            r += chr(int(s[i*anz_bit:(i+1)*anz_bit], 2))
        if len(s)%anz_bit != 0:
            r += chr(int(s[(len(s)//anz_bit)*anz_bit:], 2))
        return r

def IntToBit(x:int, lenght = 8):
        return "0"*((math.ceil((len(bin(x))-2)/lenght)*lenght+2)-len(bin(x))) + bin(x)[2:]



class Verschlüsselung():
    def __init__(self, chunk = 16, debug = True) -> None:
        """
        Text und Key als str von 0/1
        """
        self.debug = debug
        self.chunk = chunk
        #way : True -> Ent; False -> Ver


    def get_key(self, KEY:str, text=""):
        S = KEY
        S2 = []
        S3 = []
        zahl2 = 0
        zahl = 0

        key_start = 0
        key_m_cube = ""
        key_normal = []
        key_mix = 0
        #self.key_wave = {"chunk":[],"number":[],"extra":[]}# ? ? ? | sin; cos; tan; cot; sek; cosek; ^1/x; 1/x; ...
        key_len = 5

        for i in range(len(S)//key_len):
            S2.append(S[i*key_len:(i+1)*key_len])
        if len(S)%key_len != 0:
            S2.append(S[(len(S)//key_len)*key_len:])
        if len(S2[-1])==1: S2[-1] += "0"
        if self.debug: print("S2: ",S2)

        while zahl < len(S2):
            if (zahl < len(S2)) and (S2[zahl][0] == "0"):
                if int(S2[zahl][1:]) != 0:
                    zahl2 = int(S2[zahl][1:], 2)
                    zahl += 1
                    while (zahl < len(S2)) and (S2[zahl][0] == "0"):
                        zahl2 = zahl2*10**len(str(int(S2[zahl][1:], 2))) + int(S2[zahl][1:], 2)
                        zahl += 1
                else:
                    zahl2 = int(S2[zahl][1:], 2)
                    zahl += 1
                    while (zahl < len(S2)) and (S2[zahl][0] == "0"):
                        zahl2 = zahl2 + int(S2[zahl][1:], 2)*(1/10)**len(str(zahl2))
                        zahl += 1
                S3.append(zahl2)
                key_mix += zahl2
            if (zahl < len(S2)) and (S2[zahl][0] == "1"):
                if int(S2[zahl][1:]) != 0:
                    zahl2 = int(S2[zahl][1:], 2)
                    zahl += 1
                    while (zahl < len(S2)) and (S2[zahl][0] == "1"):
                        zahl2 = zahl2*10**len(str(int(S2[zahl][1:], 2))) + int(S2[zahl][1:], 2)
                        zahl += 1
                else:
                    zahl2 = int(S2[zahl][1:], 2)
                    zahl += 1
                    while (zahl < len(S2)) and (S2[zahl][0] == "1"):
                        zahl2 = zahl2 + int(S2[zahl][1:], 2)*(1/10)**len(str(zahl2))
                        zahl += 1
                S3.append(zahl2)
                key_mix += zahl2
        if len(S3) == 1: S3 = [int(S[:len(S)//2], 2), int(S[len(S)//2:], 2)]

        for i in range(1, (len(S3)-1)): key_normal.append(round(S3[i])+1)
        if len(S3) == 2: key_normal.append(int(S3[1]))


        if key_mix>1: key_mix = int(key_mix%len(BitToStr(text, self.chunk)))
        else: key_mix = int((key_mix*len(BitToStr(text, self.chunk)))%len(BitToStr(text, self.chunk)))

        key_start = int(S3[0]%len(BitToStr(text, self.chunk))) if S3[0]>=0 else int((S3[0]*len(BitToStr(text, self.chunk)))%len(BitToStr(text, self.chunk)))
        if self.debug: print("S3: ",S3)
        key_m_cube = self.get_key_m_cube(key_normal=key_normal, text=text)

        if self.debug: print("key_normal: ", key_normal, "\nstart: ", key_start, "\nmix: ", key_mix, "\nm_cube: ", key_m_cube, "\n")
        return {"n":key_normal, "s":key_start, "m":key_mix, "c":key_m_cube}

    def get_key_m_cube(self, key_normal, text=""):
        total = 0
        key_m_cube = ""
        part = []
        for i in key_normal:
            total += i
        for i in range(len(text)):
            part.append("")
            if i + total > len(text)-1:
                key_m = 1
                i2 = -1
                while (i + total - (len(text)-1))>key_m:
                    if i2 != -1:
                        part[i] = str(key_normal[i2+1]) + part[i]
                    key_m += key_normal[i2]
                    i2 -= 1
                key_m -= key_normal[i2+1]
                part[i] = str(i + total - (len(text)-1)-key_m) + part[i]
        for i in part:
            key_m_cube += i
        #evtl. umwandeln in andere Systeme
        return key_m_cube


    def entschlüsseln(self, text="", KEY = "") -> str:
        """
        entschlüsseln des Textes
        way=True
        """
        keys = self.get_key(KEY=KEY, text=text)
        if self.debug: print("\n--- ENTSCHLÜSSELN ---\n")

        if self.debug: print("original:        ", text, "\n")
        text = self.structure_mix_letter(way=True,full_text_=text, key=keys["m"])
        if self.debug: print("nach mix_letter: ", text, "\n")

        text_part = text[0:keys["s"]*self.chunk]
        text_part = text_part[::-1]
        text_part = (self.structure_m1(way=True, text=text_part, key=keys["n"].copy()))
        text_part = text_part[::-1]
        text = text[keys["s"]*self.chunk:]
        text = text_part + text#erw1

        if self.debug: print("nach erw1:       ", text, "\n")
        text = self.structure_m1(way=True, text=text, key=keys["n"].copy())
        if self.debug: print("nach m1:         ", text, "\n")

        #if self.debug: print(BitToStr(text, self.chunk))
        return text

    def verschlüsseln(self, text="", KEY = "") -> str:
        """
        verschlüsseln des Textes
        way=False
        """ 
        keys = self.get_key(KEY=KEY, text=text)
        if self.debug: print("\n--- VERSCHLÜSSELN ---\n")

        if self.debug: print("original:        ", text, "\n")
        text = self.structure_m1(way=False, text=text, key=keys["n"].copy())
        if self.debug: print("nach m1:         ", text, "\n")

        text_part = text[0:keys["s"]*self.chunk]
        text_part = text_part[::-1]
        text_part = (self.structure_m1(way=False, text=text_part, key=keys["n"].copy()))
        text_part = text_part[::-1]
        text = text[keys["s"]*self.chunk:]
        text = text_part + text#erw1

        if self.debug: print("nach erw1:       ", text, "\n")
        text = (self.structure_mix_letter(way=False, full_text_=text, key=keys["m"]))
        if self.debug: print("nach mix_letter: ", text, "\n")

        #if self.debug: print(BitToStr(text, self.chunk))
        return text


    def VER_1(self, text:list, key:list, part:str, pos:int):
        """
        Ver- und Entschlüsseln nach Methode 1
        key umgedreht!
        """
        go_on=True
        for i in range(len(key)):
            if not(go_on):
                break
            if i%2 == 0:
                for i2 in range(key[i]):
                    pos-=1
                    if pos < 0:
                        go_on = False
                        break
                    part = IntToBit((int(part, 2)^int(text[pos][:len(part)], 2)), len(part))

            else: 
                pos-=key[i]
                if pos < 0:
                    go_on = False

        return part

    def mix_letter(self,way,text,key:list):
        if len(key) == 1: key.insert(0, 2)
        length = max(key)
        length2 = math.ceil(len(text)/length)
        if way:#ENT
            key_ = [key.index(i+1)+1 for i in range(length)]
            for i in range(length2):
                sort_text = []

                if (i+1)*length >= len(text): 
                    s2, key = key.copy()[:len(text) - i*length], key[:len(text) - i*length]
                    s2.sort()
                    for i2 in range(len(s2)): key[key.index(s2[i2])] = i2+1
                    key_ = [key.index(i2+1)+1 for i2 in range(max(key))]

                for i2 in range(length):
                    if (i*length+i2 >= len(text)) or (i2 >= len(key_)): break
                    sort_text.append((key_[i2], text[i*length+i2]))
                sort_text.sort()
                for i3 in range(len(sort_text)): text[i*length+i3] = sort_text[i3][1]
            
        else:        
            for i in range(length2):
                sort_text = []
                for i2 in range(length):
                    if (i*length+i2 >= len(text)) or (i2 >= len(key)): break
                    sort_text.append((key[i2], text[i*length+i2]))
                sort_text.sort()
                for i3 in range(len(sort_text)): text[i*length+i3] = sort_text[i3][1]

        return text


    def structure_mix_letter(self, way:bool, key:int, full_text_:str) -> str:
        """
        erzeugung und anpassung des Schlüssels + Text
        """
        chunk = 4 #?
        full_text = list(BitToStr(full_text_, chunk))
        #erzeugung und anpassung des Schlüssels + Text
        key_ = key
        go_on = True
        text_end = False
        key_mix = [full_text[key_]]
        last_number = ""
        while go_on:
            key_+=1
            if key_ >= len(full_text):
                go_on = False
                text_end = True
            else:
                try:
                    key_mix.index(full_text[key_])
                    go_on=False
                    last_number = full_text[key_]
                except:
                    key_mix.append(full_text[key_])

        key_mix_copy = key_mix.copy()
        if last_number != "": key_mix_copy.append(last_number)
        for i in range(len(key_mix)): key_mix[i] = int(StrToBit(key_mix[i], lenght=chunk)[0],2) + 1
        s2 = key_mix.copy()
        s2.sort()
        for i in range(len(s2)):
            key_mix[key_mix.index(s2[i])] = i+1
        if self.debug: print("key_mix: ",key_mix)

        text_part1 = full_text[:key]
        if self.debug: print("Text_part_1 (1): ",text_part1)
        if not(text_end):
            text_part2 = full_text[key_+1:]
            if self.debug: print("Text_part_2 (1): ",text_part2)
               
        for i in range(len(key_mix)):#keine Zahl doppelt?
            if key_mix.count(key_mix[i]) != 1:
                key_mix.pop(i)

        text_part1 = self.mix_letter(way=way,text=text_part1,key=key_mix)
        if self.debug: print("Text_part_1 (2): ",text_part1)
        full_text = text_part1
        full_text.extend(key_mix_copy)
        if not(text_end):
            text_part2 = self.mix_letter(way=way,text=text_part2,key=key_mix)
            if self.debug: print("Text_part_2 (2): ",text_part2)      
            full_text.extend(text_part2)
        if self.debug: print("text: ",full_text,"#")
        return "".join(i for i in StrToBit(full_text, lenght=chunk)[0])

    def structure_m1(self, way, text:str, key:list) -> str:
        """
        struktur zum ver- und entschlüsseln der Methode 1
        """
        #print("ver- oder entschlüsseln...")
        text_ = []
        for i in range(len(text)//self.chunk):
            text_.append(text[i*self.chunk:(i+1)*self.chunk])
        if len(text)%self.chunk != 0:
            text_.append(text[(len(text)//self.chunk)*self.chunk:])
        text_2 = text_.copy()
        if len(key)>=2: key.reverse()
        if not(way):#ver
            for i in range(len(text_)): text_[i] = self.VER_1(text=text_2, key=key, part=text_[i], pos=i)
        else:#ent
            for i in range(len(text_)): text_[i] = self.VER_1(text=text_, key=key, part=text_[i], pos=i)
        text_r = ""
        for i in text_: text_r += i
        return text_r


Y_N_list = []
N_list = []

def run_test():
    global Y_N_list
    #print("new process")
    debug = True
    x = Verschlüsselung(debug=debug)

    test = "01001000011000010110110001101100011011111100100110110110"
    key = "01001000011000010110110001101100011011111100100110110110"
    test_2 = "0000110101001001101110110011001101001011101000010111101111101101100001011010010001110110011110101010111110100001011100111101001101101111111100000101001001100100000001011110000101000000100100101001110101100100101010000111111000111101001111001010101100101111011000000000001010101000100010101000011000001111010001001000000111110101000100001001100100111001110000011000010111101001100100110110110101100000011100010101111111101000001011110100000010010110110100100110100011000100011100000111111111010001110100011000011001001001110011011010101111000001111001001001000000001101010010010011111111111000111110111110110111010100101000111111100111100100100111100110000101000001100011100111000110111010011000110111110101011001001001110111111110111001100001000011101010011111111110010010110010101111010111000110100010101100111110001000101101100011000001101101001000000001011001101010010010001110000110100001000000000011100011001111001111100110110100001011001111110011110111110101101110100100011111100001010000011011001111011001111111111100110011101001010101010101101111001100000010111110010110001001010100110111111111100101111001010111111001011110010110110100110011001111011100110010001110110000101000010111100100011010010000101100000001101011000011110000001000111000101001111110010011000111001101100110111010001100100000001111100111111101111001110001100011110010111010010100110001100010111100001011101111111111101111111101111110111111100100110011010011111100001001101110110010011101100101101000101110111010110111110010000001010111011101100011010000011000000110101100001010011110000001111001111100011001000101000110011110001101010010001000000101111011001101000000011110010000010000001001100110000111001111111100111100001111000000110101011100011111010100110010100111100010111111001110111111001011110101010001000111110100000110100010100111110100100110111110111011010101001110101010110010100000011101000000101101101101000010111100000011101100011101110011100111100110111000101010000010000111100110001100001101100001110011000011010101100100011010101001011101010100011111000110001011111100111010000111011110011010010111010011001001011101010110011010110010101101110011000010100000100000001111101000000101101011011111000110010100001010010110101001010010011011111010101001011010011101001010110010100010001010000001111110010011001000001101001111110000000110110001111001110111001000010001111010111111110000101010110101000110110101010010110101011100111101101101111000000110010010001101101100111001011100100100011001111001001101110000000100010000101011000111001010101101111111011101011111111111010000000110100101111010100000000001110100010111101110010010111110000000000001100101101110111101100111001110010101000111000001110111101101101111000111111011011111100000001101010001001101000101110100110111110010101100101000101010011000110111110001110011111111111111010111101000111001111110011011101010011110110000101000110001110110010111010100100110111110110110001110110110110011010000010111110000000101111000101100000011110110110001111101101101000101101000011110111111010101010010010111000001010010100010101011100101011110101000101010101001000100101100100011011010100000101111100001100011000110111000111010011101111100111111100010101111100111000111101010011111001101000101010100101100000000111111010101111011000110110001101100101000010110100100010101010001011110110101000110100010001001111011111011010110000111011001110110001010000010000101010000011010010000100010100100111110111001011101011100000111001101110000000100001110001011001100011110110001011110111101001001101110000110101100001111010001100010110111101011110101010011001001000100111010101110101110001111100010111001110100010101001001100111110111111110010101101010000111010101100010111110000011101100010011100010011011001000101111110111000010110010011100110111000010111111011010101101100101101010011000111100110101100000100111111110000011011111010110111111111011100001101111000101011100110110110010010001101101011010001110111000100010011110000100101001000000001010111011100001010101110111101111110110010010100000000100001001101011100101111001111100111110101011010000000001100100001010000000100101011010000011001110111000101000101011111000001110010110111100111111010010101100110100101100001100101110100011011001101001101010001011110001000111110100000010010011000001100000000011001000110001100101001011000111000011111000011010000111110010001100111011001111110000001000100010101011111110100100010001011000111001101100110100000000011111111110110101101110100001010101111000010000010011101110110011010110001100001101110101100001110001110011111110101110011011100100010000110101101100000110101100101100111111010110000000110110111100011010010011000110100001010111000011111011111111111111010110010011011011010100011101100100111110001100111101011111100101011101111010111000011001100111100110100100100100101011110100011101110101001101011100100001001011010110010000110001011001101011110101100110000101000011111100001001011000101010110101110000111100000011001011000011010011001101101101111011010011011100100010011111001111101000001001100100011011011101110111100001101010111100010000101001111011110110001100101010111100110001011001010000011010000010110101000001001000110011010001101010010101101011010011010000011011100011001000100000110100000110010001011100111101100010110011001010101011000011000001010001111100000110111100110111110011111001110101010011011010000110010010011110110000110000011100111100100011101010010000001111101111010101100101101101010001010110110001000100101100010100111100100010000111101011110011000100000100100000001011011110011100001001111101010011101000001110001100110001101011110100101100001010100101111111001110101111110101101000101010111010100100011010100111100111101001101100110101111010001000110000000101011111000000110001100101100001001011010100100101001010000001111101010000001101001010000011001010000100011111110011110001000111000010010101000010011111011100011001100011001110011111100010011010001100001010010001010110000110110110001001000000101101011110111001010010101111100000000001111010000100101111000100100111011010101001001110111001010000011011101011100010000111011110010111010000101011001011111010011110110001011000001101101011000110101100111001111100011000110001100100101110010110001110111110011011000011101000001011011011100011001110010100111000111010100011001110111110011101110001111001110100011100111100101011100011110100000000110000100001111011111100"
    #for i in range(6400): test += str(randint(0, 1))
    #for i in range(20): key += str(randint(0, 1))

    #if debug: print(test)
    if test == x.entschlüsseln(x.verschlüsseln(text=test, KEY=key), key): Y_N_list.append("Y")
    else: Y_N_list.append("N"); N_list.append((test, key))

if __name__ == "__main__":
    p=[]
    t = time.time()
    for i in range(1):
        """p.append(multiprocessing.Process(target = run_test))
        p[i].start()
        p[i].join()"""
        run_test()
    t = time.time() - t
    print("Y:", Y_N_list.count("Y"), "|", "N:", Y_N_list.count("N"), "|", "D:", t)
    print(N_list)
    #print(IntToBit(int(IntToBit((int("00001101010010011011", 2)^int("1011001100110100", 2))), 2)^int("00001101010010011011", 2)))



"""
xor bit:

x = "10101010"
y = "01010101"
z = bin(int(x,2)^int(y,2))[2:]


with open(<name>, "rb") as f:
    test_content = f.read()

test_content_arr = []
for i in test_content:
    test_content_arr.append(i)
print(test_content_arr)

test2_content = bytes(test_content_arr)
with open(<name>, "wb") as f:
    f.write(test2_content)
"""
class fehler(ValueError): ...
