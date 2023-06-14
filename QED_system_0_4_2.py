import math
from random import randint
import time

def StrToBit(x:str|list, lenght = 8):
        text = ""
        for i in x:
            text += "0"*((math.ceil((len(bin(ord(i)))-2)/lenght)*lenght+2)-len(bin(ord(i)))) + bin(ord(i))[2:]
        return text

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

    def get_key_m_cube(self, key_normal, text=""):#!?
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
        #text = self.structure_mix_letter(way=True,full_text_=text, key=keys["m"])
        #if self.debug: print("nach mix_letter: ", text, "\n")

        text_part = text[:keys["s"]*self.chunk]
        text_part = text_part[::-1]
        text_part = self.structure_m1(way=True, text=text_part, key=keys["n"].copy())
        text_part = text_part[::-1]
        text_ = text[keys["s"]*self.chunk:]
        text = text_part + text_#erw1

        if self.debug: print("nach erw1:       ", text, "\n")
        text = self.structure_m1(way=True, text=text, key=keys["n"].copy())
        if self.debug: print("nach m1:         ", text, "\n")

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

        text_part = text[:keys["s"]*self.chunk]
        text_part = text_part[::-1]
        text_part = self.structure_m1(way=False, text=text_part, key=keys["n"].copy())
        text_part = text_part[::-1]
        text_ = text[keys["s"]*self.chunk:]
        text = text_part + text_#erw1

        if self.debug: print("nach erw1:       ", text, "\n")
        #text = (self.structure_mix_letter(way=False, full_text_=text, key=keys["m"]))
        #if self.debug: print("nach mix_letter: ", text, "\n")

        return text


    def VER_1(self, text:list, text_:list, anz:int, i:int, start:int, way:bool) -> list:
        """
        Ver- und Entschlüsseln nach Methode 1
        """
        if way:
            for i2 in range(anz):#ent
                if start+i2 >= len(text): break
                text[start+i2]=IntToBit(int(text[start+i2])^int(text[i]))
        elif not(way):
            for i2 in range(anz):#ver
                if start+i2 >= len(text): break
                text[start+i2]=IntToBit(int(text[start+i2])^int(text_[i]))
        return text

    def mix_letter(self,way,text:list,key:list) -> list:
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
            
        else:#VER
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
        for i in range(len(text_)-1):
            start=0
            for i2 in range(len(key)):
                if i+start+1 >= len(text_): break
                if i2%2 ==1:
                    start+=key[i2]
                else:
                    text_ = self.VER_1(text=text_, text_=text_2 ,i=i, anz=key[i2], start=i+start+1, way=way)
                    start+=key[i2]
        text_r = ""
        for i in text_: text_r += i
        return text_r



Y = 0
N = 0
N_list = []

def run_test():
    global Y
    global N
    #print("new process")
    debug = False
    x = Verschlüsselung(debug=debug)

    test = ""
    key = ""
    l1 = 1600#randint(10, 1600)
    l2 = 100#randint(20, 100)
    for i in range(l1*4): test += str(randint(0, 1))
    for i in range(l2): key += str(randint(0, 1))

    #if debug: print(test)
    if test == x.entschlüsseln(x.verschlüsseln(text=test, KEY=key), key): Y+=1
    else: N+=1; N_list.append((test, key))

if __name__ == "__main__":
    p=[]
    t = time.time()
    for i in range(100):
        """p.append(multiprocessing.Process(target = run_test))
        p[i].start()
        p[i].join()"""
        run_test()
    t = time.time() - t
    print("Y:", Y, "|", "N:", N, "|", "D:", t)
    #print(N_list)



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
