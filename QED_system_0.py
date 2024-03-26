import math
from random import randint

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


    def get_key(self, KEY:str, texts={"o":"", "v":"", "e":""}):
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
        key_len = 9

        for i in range(len(S)//key_len):
            S2.append(S[i*key_len:(i+1)*key_len])
        if len(S)%key_len != 0:
            S2.append(S[(len(S)//key_len)*key_len:])
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
 
        for i in range(1, (len(S3)-1)): key_normal.append(S3[i])
        if len(S3) == 2: key_normal.append(S3[1])

        key_mix = key_mix%len(BitToStr(texts["o"], self.chunk))
        key_start = S3[0] if S3[0]>=0 else S3[0]*len(BitToStr(texts["o"], self.chunk))
        if self.debug: print("S3: ",S3)
        key_m_cube = self.get_key_m_cube(key_normal=key_normal, texts=texts)

        if self.debug: print("key_normal: ", key_normal, "\nstart: ", key_start, "\nmix: ", key_mix, "\nm_cube: ", key_m_cube, "\n")
        return {"n":key_normal, "s":key_start, "m":key_mix, "c":key_m_cube}

    def get_key_m_cube(self, key_normal, texts={"o":"", "v":"", "e":""}):
        total = 0
        key_m_cube = ""
        part = []
        for i in key_normal:
            total += i
        for i in range(len(texts["o"])):
            part.append("")
            if i + total > len(texts["o"])-1:
                key_m = 1
                i2 = -1
                while (i + total - (len(texts["o"])-1))>key_m:
                    if i2 != -1:
                        part[i] = str(key_normal[i2+1]) + part[i]
                    key_m += key_normal[i2]
                    i2 -= 1
                key_m -= key_normal[i2+1]
                part[i] = str(i + total - (len(texts["o"])-1)-key_m) + part[i]
        for i in part:
            key_m_cube += i
        #evtl. umwandeln in andere Systeme
        return key_m_cube


    def entschlüsseln(self, text="", KEY = ""):
        """
        entschlüsseln des Textes
        way=True
        """
        texts = {"o": text, "v": text, "e": text}
        keys = self.get_key(KEY=KEY, texts=texts)
        if self.debug: print("\n--- ENTSCHLÜSSELN ---\n")
        texts["e"] = self.structure_mix_letter(way=True,full_text_=texts["e"], key=keys["m"])
        texts["e"] = (self.structure_m1(way=True, text=texts["e"][0:keys["s"]][::-1], key=keys["n"]))[::-1] + texts["e"][keys["s"]:]#erw1
        texts["e"] = self.structure_m1(way=True, text=texts["e"], key=keys["n"])

        if self.debug: print(BitToStr(texts["e"], self.chunk))
        return texts["e"]

    def verschlüsseln(self, text="", KEY = ""):
        """
        verschlüsseln des Textes
        way=False
        """
        texts = {"o": text, "v": text, "e": text}
        keys = self.get_key(KEY=KEY, texts=texts)
        if self.debug: print("\n--- VERSCHLÜSSELN ---\n")
        texts["v"] = self.structure_m1(way=False, text=texts["v"], key=keys["n"])
        texts["v"] = (self.structure_m1(way=False, text=texts["v"][0:keys["s"]][::-1], key=keys["n"]))[::-1] + texts["v"][keys["s"]:]#erw1
        texts["v"] = (self.structure_mix_letter(way=True, full_text_=texts["v"], key=keys["m"]))

        if self.debug: print(BitToStr(texts["v"], self.chunk))
        return texts["v"]


    def VER_1(self, text:list, key:list, part:str, pos:int):#verbessern!!!!
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
                    part = IntToBit(int(part)^int(text[pos]))
            else: 
                pos-=key[i]
                if pos < 0:
                    go_on = False

        return part


    def mix_letter(self,way,text,key:list):
        length = max(key)
        ausgabe = []
        if way:#ENT
            for i in range(len(text)//length + 1):
                if int((i+1)*length) <= len(text):
                    for i2 in key:
                        i2 -= 1
                        try:
                            ausgabe.append(str(text[i*length + i2]))
                        except:
                            pass
                else:
                    new_key = []
                    x = 0
                    for i2 in range(len(text) - int(i*length)): 
                        new_key.append(key[i2])
                    new_key3 = new_key.copy()
                    new_key2 = new_key.copy()
                    new_key2.sort()
                    for i2 in range(len(new_key)):
                        new_key[new_key3.index(new_key2[i2])]=x
                        x += 1
                    if self.debug: print("keys: ", new_key, new_key3)
                    for i2 in new_key:
                        try:
                            ausgabe.append(str(text[i*length + i2]))
                        except:
                            pass

        else:#VER
            z=0
            ausgabe = []
            length2 = length
            while length2 < len(text): length2 += length
            for i in range(length2):
                ausgabe.append("¿")
            dump = int(len(text)/length) + 1
            for i in range(dump):
                for i2 in range(len(key)):
                    try:
                        ausgabe[i*length + key[i2] - 1] = text[i*length+i2]
                    except Exception as e:
                        pass
            
        return ausgabe


    def structure_mix_letter(self, way:bool, key:str, full_text_:str):#VERBESSERN!!!
        """
        erzeugung und anpassung des Schlüssels + Text
        """
        #chunk = 4 #?
        full_text = list(BitToStr(full_text_, self.chunk))
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
        for i in range(len(key_mix)): key_mix[i] = int(StrToBit(key_mix[i])[0],2) + 1
        s2 = key_mix.copy()
        s2.sort()
        if s2[-1] > len(key_mix):#restlichen Zahlen hinzufügen
            for i in range(1, s2[-1]):
                try:
                    key_mix.index(i)
                except:
                    key_mix.append(i)
        if self.debug: print("key_mix: ",key_mix)

        text_part1 = full_text[:key]
        if self.debug: print("Text_part_1 (1): ",text_part1)
        if not(text_end):
            text_part2 = full_text[key_+1:]
            #text_part2.append(full_text[-1])
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
        return "".join(i for i in StrToBit(full_text)[0])
        #self.info_log += f"code: mix_total; in: {self.info_location}; at: {time.asctime()} -> {e}\n"

    def structure_m1(self, way, text:str, key:list):# Verschnellern!
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
        if len(key)>=2: key=key.reverse()
        if not(way):#ver
            for i in range(len(text_)): text_[i] = self.VER_1(text=text_2, key=key, part=text_[i], pos=i)
        else:#ent
            for i in range(len(text_)): text_[i] = self.VER_1(text=text_, key=key, part=text_[i], pos=i)
        return text

debug = True
x = Verschlüsselung(debug=debug)
test = ""
key = ""
for i in range(50): test += str(randint(0, 1))
for i in range(18): key += str(randint(0, 1))

if debug: print(test)
if test == x.entschlüsseln(x.verschlüsseln(text=test, KEY=key), key): print("Y")
else: print("N")


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