import math
from random import randint
import time
import multiprocessing

def BitToInt(s:str, anz_bit= 8) -> list:
        r= []
        for i in range(len(s)//anz_bit):
            r.append(int(s[i*anz_bit:(i+1)*anz_bit], 2))
        if len(s)%anz_bit != 0:
            r.append(int(s[(len(s)//anz_bit)*anz_bit:], 2))
        return r


class Verschlüsselung():
    def __init__(self, chunk = 16, debug = True, cube_field_data_size = 1, debug_c=False, debug_f=False) -> None:
        """
        debug_c -> debug für cube class
        debug   -> debug alles andere
        chunk   -> größe der Blöcke für VER1
        cores   -> das Programm benötigt cores+1 Kerne! bei cores=0 funktioniert es nicht! anz der Parallel gedrehten Würfel
        cube_field_data_size -> größe der strings die auf ein Feld der Würfel geschrieben werden
        """
        self.debug = debug
        self.chunk = chunk
        self.cube_field_data_size = cube_field_data_size
        self.debug_c = debug_c
        self.debug_f = debug_f

    def get_key(self, KEY:str, text=""):
        """
        erzeugt aus KEY(str aus 0/1) und text(str aus 0/1)
        -> key_start:int; key_m_cube:int; key_normal:list; key_mix:int
        ruft für key_m_cube  get_key_m_cube  auf

        key_len wir hier gesetzt
        """
        S = KEY
        S2 = []
        S3 = []
        zahl2 = 0
        zahl = 0

        key_start = 0
        key_m_cube = 0
        key_normal = []
        key_mix = 0
        key_len = 5#-----------------------------------------------------------------------------------------------------------

        for i in range(len(S)//key_len):
            S2.append(S[i*key_len:(i+1)*key_len])
        if len(S)%key_len != 0:
            S2.append(S[(len(S)//key_len)*key_len:])
        if len(S2[-1])==1: S2[-1] += "0"
        if self.debug: print("S2: ",S2)

        while zahl < len(S2):
            if (zahl < len(S2)) and (S2[zahl][0] == "0"):
                if int(S2[zahl][1:]) != 0:
                    zahl2 = S2[zahl][1:]#-----------------------------------------------------------------------------
                    zahl += 1
                    while (zahl < len(S2)) and (S2[zahl][0] == "0"):
                        zahl2 += S2[zahl][1:]#---------------------------------------------------------------------
                        zahl += 1
                    zahl2 = int(zahl2, 2)

                else:
                    zahl2 = "0"#-----------------------------------------------------------------------------
                    zahl += 1
                    while (zahl < len(S2)) and (S2[zahl][0] == "0"):
                        zahl2 += S2[zahl][1:]
                        zahl += 1
                    zahl2 = float(f"0.{int(zahl2, 2)}")
                S3.append(zahl2)
                key_mix += zahl2


            if (zahl < len(S2)) and (S2[zahl][0] == "1"):
                if int(S2[zahl][1:]) != 0:
                    zahl2 = S2[zahl][1:]#-----------------------------------------------------------------------------
                    zahl += 1
                    while (zahl < len(S2)) and (S2[zahl][0] == "1"):
                        zahl2 += S2[zahl][1:]#---------------------------------------------------------------------
                        zahl += 1
                    zahl2 = int(zahl2, 2)

                else:
                    zahl2 = "0"#-----------------------------------------------------------------------------
                    zahl += 1
                    while (zahl < len(S2)) and (S2[zahl][0] == "1"):
                        zahl2 += S2[zahl][1:]
                        zahl += 1
                    zahl2 = float(f"0.{int(zahl2, 2)}")
                S3.append(zahl2)
                key_mix += zahl2


        if len(S3) == 1: S3 = [int(S[:len(S)//2], 2), int(S[len(S)//2:], 2)]

        for i in range(1, len(S3)): key_normal.append(round(S3[i])+1)
        if len(S3) == 2: key_normal.append(int(S3[1]))

        if key_mix>=1: key_mix = int(key_mix%math.ceil(len(text)/self.chunk))
        else: key_mix = int(key_mix*math.ceil(len(text)/self.chunk))

        key_start = int(S3[0]%math.ceil(len(text)/self.chunk)) if S3[0]>=1 else int(S3[0]*math.ceil(len(text)/self.chunk))
        
        if self.debug: print("S3: ",S3)
        
        key_m_cube = self.get_key_m_cube(key_normal=key_normal.copy(), key_start=key_start)
        
        #if len(key_normal)%2 == 0: key_normal = key_normal[:len(key_normal)-1]

        if self.debug: print("key_normal: ", key_normal, "\nstart: ", key_start, "\nmix: ", key_mix, "\nm_cube: ", key_m_cube, "\n")
        return {"n":key_normal, "s":key_start, "m":key_mix, "c":key_m_cube}

    def get_key_m_cube(self, key_normal:list, key_start:int, g=250) -> int:
        """
        erzeugt aus key_normal und key_start
        -> key_m_cube

        g -> ungefähre länge im 18er system
        """
        key_m_cube = ""
        if sum(key_normal) > key_start:
            while key_start > 0:
                if key_start - key_normal[0] > 0:
                    key_start -= key_normal[0]
                    key_normal.pop(0)
                else:
                    key_normal[0] -= key_start
                    key_start = 0
        else:
            pass#???

        key_m_cube = int("".join(str(i) for i in key_normal))
        #umwandeln in andere Systeme
        key_m_cube = self.hilfsfunktionen.int2anybase(number=key_m_cube,base=5)
        key_m_cube = [key_m_cube[i]+key_m_cube[i+1] for i in range(0, len(key_m_cube)//2, 2)]# + %10 ?
        key_m_cube = self.hilfsfunktionen.anybase2anybase(key_m_cube, 9, 10)

        while len(key_m_cube) < g:
            key_m_cube = int("".join(str(i) for i in key_m_cube))
            key_m_cube = self.hilfsfunktionen.int2anybase2(number=key_m_cube, base=1.7)
            key_m_cube = "".join(str(i*10).split(".")[0] for i in key_m_cube)
            key_m_cube = [int(i) for i in key_m_cube]
        while len(key_m_cube) > g*1.75:
            key_m_cube = self.hilfsfunktionen.anybase2anybase(number_=key_m_cube, input_base=10, output_base=5)# 5 -> ?
            key_m_cube = [key_m_cube[i]+key_m_cube[i+1] for i in range(0, len(key_m_cube)//2, 2)]# + %10 ?
            key_m_cube = self.hilfsfunktionen.anybase2anybase(key_m_cube, 9, 10)
        key_m_cube = int("".join(str(i) for i in key_m_cube))

        return key_m_cube

    def entschlüsseln(self, text="", KEY = "") -> str:
        """
        entschlüsselt den Text mit KEY
        -> text:str
        way=True
        """
        keys = self.get_key(KEY=KEY, text=text)
        if self.debug: print("\n--- ENTSCHLÜSSELN ---\n")
        if self.debug: print("original:        ", text, "\n")
        if self.debug_f: 
            with open("ENT_0_original.txt", "wb") as f:
                f.write(bytes(BitToInt(text)))


        text = self.mix_letter(way=True,full_text_=text, key=keys["m"])
        if self.debug: print("nach mix_letter: ", text, "\n")
        if self.debug_f: 
            with open("ENT_1_nach_mix_letter.txt", "wb") as f:
                f.write(bytes(BitToInt(text)))


        text_part = text[:keys["s"]*self.chunk]
        text_part = text_part[::-1]
        text_part = self.VER_1(way=True, text=text_part, key=keys["n"].copy())
        text_part = text_part[::-1]
        text_ = text[keys["s"]*self.chunk:]
        text = text_part + text_#erw1
        if self.debug: print("nach erw1:       ", text, "\n")
        if self.debug_f: 
            with open("ENT_2_nach_m1_2.txt", "wb") as f:
                f.write(bytes(BitToInt(text)))


        text = self.cube(text=text, key_m_cube=keys["c"], encryption=not(True))
        if self.debug: print("nach cube:       ", text, "\n")
        if self.debug_f: 
            with open("ENT_3_nach_cube.txt", "wb") as f:
                f.write(bytes(BitToInt(text)))


        text = self.VER_1(way=True, text=text, key=keys["n"].copy())
        if self.debug: print("nach m1:         ", text, "\n")
        if self.debug_f: 
            with open("ENT_4_nach_m1.txt", "wb") as f:
                f.write(bytes(BitToInt(text)))

        return text

    def verschlüsseln(self, text="", KEY = "") -> str:
        """
        verschlüsselt den Text mit KEY
        -> text:str
        way=False
        """ 
        keys = self.get_key(KEY=KEY, text=text)
        if self.debug: print("\n--- VERSCHLÜSSELN ---\n")
        if self.debug: print("original:        ", text, "\n")
        if self.debug_f: 
            with open("VER_0_original.txt", "wb") as f:
                f.write(bytes(BitToInt(text)))

        text = self.VER_1(way=False, text=text, key=keys["n"].copy())
        if self.debug: print("nach m1:         ", text, "\n")
        if self.debug_f: 
            with open("VER_1_nach_m1.txt", "wb") as f:
                f.write(bytes(BitToInt(text)))


        text = self.cube(text=text, key_m_cube=keys["c"], encryption=not(False))
        if self.debug: print("nach cube:       ", text, "\n")
        if self.debug_f: 
            with open("VER_2_nach_cube.txt", "wb") as f:
                f.write(bytes(BitToInt(text)))


        text_part = text[:keys["s"]*self.chunk]
        text_part = text_part[::-1]
        text_part = self.VER_1(way=False, text=text_part, key=keys["n"].copy())
        text_part = text_part[::-1]
        text_ = text[keys["s"]*self.chunk:]
        text = text_part + text_#erw1
        if self.debug: print("nach erw1:       ", text, "\n")
        if self.debug_f: 
            with open("VER_3_nach_m1_2.txt", "wb") as f:
                f.write(bytes(BitToInt(text)))


        text = (self.mix_letter(way=False, full_text_=text, key=keys["m"]))
        if self.debug: print("nach mix_letter: ", text, "\n")
        if self.debug_f: 
            with open("VER_4_nach_mix_letter.txt", "wb") as f:
                f.write(bytes(BitToInt(text)))

        return text


    def _VER_1(self, text:list, key:list, part:str, pos:int) -> str:
        """
        xor der Bits von part mit den von text nach key
        pos = position von part im text

        key umgedreht eingeben!
        """
        go_on = True
        i = 0
        while go_on:
            if i >= len(key):
                i = 0
            if i%2 == 0:
                for i2 in range(key[i]):
                    pos-=1
                    if pos < 0:
                        go_on = False
                        break
                    part = self.hilfsfunktionen.IntToBit((int(part, 2)^int(text[pos][:len(part)], 2)), len(part))
            else: 
                pos-=key[i]
                if pos < 0:
                    go_on = False
            i += 1

        return part

    def _mix_letter(self,way,text:list,key:list) -> list:
        """
        mischt den text mit key
        way = richtung
        """
        if len(key) == 1: key.insert(0, 2)
        length = len(key)
        length2 = math.ceil(len(text)/length)
        if way:#ENT
            key_ = [key.index(i+1)+1 for i in range(length)]
            for i in range(length2):

                if (i+1)*length >= len(text): # schlüssel für kürzere Textabschnitte anpassen
                    key = key[:len(text) - i*length]
                    s2, key = key.copy()[:len(text) - i*length], key[:len(text) - i*length]
                    s2.sort()
                    for i2 in range(len(s2)): key[key.index(s2[i2])] = i2+1 # kleinste Zahl -> 1, ...
                    key_ = [key.index(i2+1)+1 for i2 in range(max(key))] # key-ver -> key-ent

                text[i*length:(i+1)*length] = [x for _,x in sorted(zip(key_, text[i*length:(i+1)*length]))]
            
        else:        
            for i in range(length2):
                text[i*length:(i+1)*length] = [x for _,x in sorted(zip(key, text[i*length:(i+1)*length]))]

        return text


    def mix_letter(self, way:bool, key:int, full_text_:str, chunk = 4) -> str:
        """
        erzeugt aus full_text_ und key einen schlüssel
        und teit den text
        ruft  mix_letter  auf
        way = richtung
        -> text vermischt
        """
        full_text = []
        for i in range(len(full_text_)//chunk):
            full_text.append(full_text_[i*chunk:(i+1)*chunk])
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
                if key_mix.count(full_text[key_]) == 0:
                    key_mix.append(full_text[key_])
                else:
                    go_on=False
                    last_number = full_text[key_]

        key_mix_copy = key_mix.copy()
        if last_number != "": key_mix_copy.append(last_number)
        for i in range(len(key_mix)): key_mix[i] = int(key_mix[i],2) + 1
        s2 = key_mix.copy()
        s2.sort()
        for i in range(len(s2)):# alle Zahel aufeinanderfolgend 1.. bsp. 5 1 3 -> 3 1 2 
            key_mix[key_mix.index(s2[i])] = i+1   
        #for i in range(len(key_mix)):#keine Zahl doppelt? | wird vorher schon überprüft
        #    if key_mix.count(key_mix[i]) != 1:
        #        key_mix.pop(i)
        if self.debug: print("key_mix: ",key_mix)

        text_part1 = full_text[:key]
        if self.debug: print("Text_part_1 (1): ",text_part1)
        if not(text_end):
            text_part2 = full_text[key_+1:]
            if self.debug: print("Text_part_2 (1): ",text_part2)
               

        text_part1 = self._mix_letter(way=way,text=text_part1,key=key_mix)
        if self.debug: print("Text_part_1 (2): ",text_part1)
        full_text = text_part1
        full_text.extend(key_mix_copy)
        if not(text_end):
            text_part2 = self._mix_letter(way=way,text=text_part2,key=key_mix)
            if self.debug: print("Text_part_2 (2): ",text_part2)      
            full_text.extend(text_part2)
        if self.debug: print("text: ",full_text,"#")
        return "".join(i for i in full_text)

    def VER_1(self, way, text:str, key:list) -> str:
        """
        struktur zum ver- und entschlüsseln der Methode 1
        """
        #print("ver- oder entschlüsseln...")
        text_ = []
        for i in range(len(text)//self.chunk):
            text_.append(text[i*self.chunk:(i+1)*self.chunk])
        if len(text)%self.chunk != 0:
            text_.append(text[(len(text)//self.chunk)*self.chunk:])
        if len(key)>=2: key.reverse()
        if not(way):#ver
            for i in range(len(text_)-1, -1, -1): text_[i] = self._VER_1(text=text_, key=key, part=text_[i], pos=i)
        else:#ent
            for i in range(len(text_)): text_[i] = self._VER_1(text=text_, key=key, part=text_[i], pos=i)
        text_r = ""
        for i in text_: text_r += i
        return text_r

    class cube_class():
        def __init__(self, dimensions=3, debug=False):
            self.dimensions = dimensions
            self.debug = debug

            self.cube = []
            for i0 in range(6):
                self.cube.append([])
                for i1 in range(self.dimensions):
                    self.cube[i0].append([])
                    for i2 in range(self.dimensions):
                        self.cube[i0][i1].append(i0)
            if self.debug:
                #print(f"self.cube: {self.cube}")
                self.print_cube()

        def rotate_array(self, arr, rotation=1):
            #print(f"rotation % 4 + 4 = {(rotation % 4) +4}")
            for i in range((rotation % 4) + 4):
                h = list(zip(*arr[::-1]))
                for i in range(len(h)):
                    h[i] = list(h[i])
                arr = h
            return(arr)
        
        def rotate(self, axis, plane, rotation):
            if axis == "z":
                rotation = 4 - rotation
            for i in range(rotation % 4):
                self._rotate(axis, plane)

        def _rotate(self, axis, plane):
            #determine fixed values for cube rotation
            if axis == "x":
                rotations = [0, 0, 0, 2]
                faces = [0, 2, 5, 4]
            elif axis == "y":
                rotations = [1, 0, 3, 2]
                faces = [0, 3, 5, 1]
            elif axis == "z":
                rotations = [1, 1, 1, 1]
                faces = [4, 3, 2, 1]

            # generate full_rotation (len = 6 &! 4)
            cube_r = []
            full_rotation = []
            for i1 in range(6):
                for i2 in faces:
                    if i2 == i1:
                        full_rotation.append(rotations[faces.index(i1)])
                if len(full_rotation) != i1 +1:
                    full_rotation.append(0)
            if self.debug:
                print(f"\nfull_rotation: {full_rotation}")

            # generate rotated cube modell
            cube_r = []
            for i in range(6):
                h_arr = self.rotate_array(self.cube[i], (full_rotation[i] +1))
                cube_r.append(h_arr)
            if self.debug:
                print(f"\ncube_r: {cube_r}")

            # rotate ring
            h2 = cube_r[faces[-1]][plane]
            for i in range(4):
                h1 = cube_r[faces[i]][plane]
                #print(f"h2 for i={i} > h1: {h2} > {h1}")
                cube_r[faces[i]] = cube_r[faces[i]]
                cube_r[faces[i]][plane] = h2
                h2 = h1
                #print(f"cube_r: {cube_r}")
            for i in range(6):
                self.cube[i] = self.rotate_array(cube_r[i], (4-full_rotation[i] -1))
            
            # rotate outer face
            rot_dict = {"x": [1,3], "y": [2,4], "z": [0,5]}
            if (plane == 0):
                self.cube[rot_dict[axis][0]] = self.rotate_array(self.cube[rot_dict[axis][0]], 1)
            elif (plane == self.dimensions-1):
                self.cube[rot_dict[axis][1]] = self.rotate_array(self.cube[rot_dict[axis][1]], 1)
        
        def print_cube(self):
            rotations = []
            for i1 in range(self.dimensions):
                for i2 in range(self.dimensions):
                    print("  ", end="")
                for i2 in range(self.dimensions):
                    print(f"{str(self.cube[0][i1][i2])} ", end="")
                print("")
            for i1 in range(self.dimensions):
                for i3 in [1,2,3,4]:
                    for i2 in range(self.dimensions):
                        print(f"{str(self.cube[i3][i1][i2])} ", end="")
                print("")
            for i1 in range(self.dimensions):
                for i2 in range(self.dimensions):
                    print("  ", end="")
                for i2 in range(self.dimensions):
                    print(f"{str(self.cube[5][i1][i2])} ", end="")
                print("")
    
    def _cube_int_to_moves(self, integer, cube_dimensions, encrypt):
        '''
        returnt ein "step_array" = [[rotate_argument_1, rotate_argument_2, rotate_argument_3], ...]
        nutzt "integer" als seed
        <encrypt> ist die "richtung", kann True oder False sein, also ob ver-/entschlüsselt wird.
        '''
        step_array = []
        seed = self.hilfsfunktionen.int2anybase(integer, cube_dimensions*3)

        '''
        for i1 in range(min(len(seed), cube_dimensions*20)):
            i = seed[i1]
            axis = ["x", "y", "z"][i%3]
            plane = i // 3
            if encrypt:
                direction = 1
            else:
                direction = -1
            step_array.append([axis, plane, direction])
        '''
        for i in seed:
            axis = ["x", "y", "z"][i%3]
            plane = i // 3
            if encrypt:
                direction = 1
            else:
                direction = -1
            step_array.append([axis, plane, direction])
        
        
        if self.debug_c:
            print(step_array)
            print(len(step_array))
        
        if not(encrypt):
            step_array.reverse()
    

        return step_array.copy()
    
    def _cube_map_data(self, cube, text, cube_field_data_size):
        '''
        mappt <text> auf cube.<cube> zu <cube_field_data_size> großen chunks
        '''
        text_pointer = 0
        for i1 in range(len(cube)):
            for i2 in range(len(cube[i1])):
                for i3 in range(len(cube[i1][i2])):
                    cube[i1][i2][i3] = text[text_pointer:(text_pointer+cube_field_data_size)]
                    text_pointer += cube_field_data_size
        
        return cube.copy()
    
    def _cube_map_data_2(self, cube, text:list, cube_field_data_size=1):
        '''
        mappt <text> auf cube.<cube> zu <cube_field_data_size> großen chunks
        '''
        text_pointer = 0
        for i1 in range(len(cube)):
            for i2 in range(len(cube[i1])):
                for i3 in range(len(cube[i1][i2])):
                    cube[i1][i2][i3] = text[text_pointer]
                    text_pointer += cube_field_data_size
        
        return cube.copy()

    def _cube_get_data(self, cube) -> str:
        '''
        nimmt cube.<cube> und returnt die daten als string
        '''
        text = ""
        for i1 in cube:
            for i2 in i1:
                for i3 in i2:
                    text += i3
        
        return text
    
    def _cube_get_data_2(self, cube) -> list:
        '''
        nimmt cube.<cube> und returnt die daten als liste
        '''
        text = []
        for i1 in cube:
            for i2 in i1:
                for i3 in i2:
                    text.append(i3)
        
        return text

    def cube(self, text, key_m_cube, cube_dimensions=0, cube_field_data_size=0, encryption=True):
        '''
        mappt <text> in <cube_field_data_size> großen stücken auf die oberfläche eines rubics-cube
        mit <cube_dimensions> "flächen" (das entscheidet also obs ein 3x3x3, 4x4x4, ... ist)

        dreht danach den würfel, abhängig von key_m_cube

        <encryption> = richtung der verschlüsselung: {True: verschlüsseln, False: entschlüsseln}

        -> return text_verdreht
        '''
        if cube_field_data_size == 0:
            cube_field_data_size = self.cube_field_data_size
        
        if (len(text) >= (20*20*6)) and encryption:
            cube_field_data_size_local = len(text) // (20*20*6)
            key_m_cube_big = self.hilfsfunktionen.int2anybase(key_m_cube, 42)
            key_m_cube_big = int(str(self.get_key_m_cube(key_m_cube_big, 343, 1000)))
            text = self.cube_big(text, key_m_cube_big, 20, cube_field_data_size_local, encryption)

        # Zerlegen in 216er Teile
        text_formatted = []
        for i in range(len(text)//216): # 6*6*6 = 216
            text_formatted.append(list(text[i*216:(i+1)*216]))
        if len(text)%216 != 0:
            text_formatted.append(list(text[(len(text)//216)*216:]))

        #step_array = self._cube_int_to_moves(key_m_cube, 6, True)
        #cube = self.cube_class(6,self.debug_c)
        #cube.cube = self._cube_map_data_2(cube.cube.copy(), [i for i in range(1, 217, 1)], 1) # 1, 217 -> 1,2,3,...215,216
        step_array = self.hilfsfunktionen.int2anybase(key_m_cube, 18)
        quick_rotate = [[180, 2, 3, 4, 5, 6, 174, 8, 9, 10, 11, 12, 168, 14, 15, 16, 17, 18, 162, 20, 21, 22, 23, 24, 156, 26, 27, 28, 29, 30, 150, 32, 33, 34, 35, 36, 67, 61, 55, 49, 43, 37, 68, 62, 56, 50, 44, 38, 69, 63, 57, 51, 45, 39, 70, 64, 58, 52, 46, 40, 71, 65, 59, 53, 47, 41, 72, 66, 60, 54, 48, 42, 1, 74, 75, 76, 77, 78, 7, 80, 81, 82, 83, 84, 13, 86, 87, 88, 89, 90, 19, 92, 93, 94, 95, 96, 25, 98, 99, 100, 101, 102, 31, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 211, 151, 152, 153, 154, 155, 205, 157, 158, 159, 160, 161, 199, 163, 164, 165, 166, 167, 193, 169, 170, 171, 172, 173, 187, 175, 176, 177, 178, 179, 181, 73, 182, 183, 184, 185, 186, 79, 188, 189, 190, 191, 192, 85, 194, 195, 196, 197, 198, 91, 200, 201, 202, 203, 204, 97, 206, 207, 208, 209, 210, 103, 212, 213, 214, 215, 216], [180, 2, 3, 4, 5, 6, 174, 8, 9, 10, 11, 12, 168, 14, 15, 16, 17, 18, 162, 20, 21, 22, 23, 24, 156, 26, 27, 28, 29, 30, 42, 41, 40, 39, 38, 37, 67, 61, 55, 49, 43, 73, 68, 62, 56, 50, 44, 182, 69, 63, 57, 51, 45, 183, 70, 64, 58, 52, 46, 184, 71, 65, 59, 53, 47, 185, 72, 66, 60, 54, 48, 186, 31, 25, 19, 13, 7, 1, 104, 98, 92, 86, 80, 74, 105, 99, 93, 87, 81, 75, 106, 100, 94, 88, 82, 76, 107, 101, 95, 89, 83, 77, 108, 102, 96, 90, 84, 78, 150, 110, 111, 112, 113, 114, 32, 116, 117, 118, 119, 120, 33, 122, 123, 124, 125, 126, 34, 128, 129, 130, 131, 132, 35, 134, 135, 136, 137, 138, 36, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 211, 151, 152, 153, 154, 155, 205, 157, 158, 159, 160, 161, 199, 163, 164, 165, 166, 167, 193, 169, 170, 171, 172, 173, 187, 175, 176, 177, 178, 179, 181, 139, 133, 127, 121, 115, 109, 79, 188, 189, 190, 191, 192, 85, 194, 195, 196, 197, 198, 91, 200, 201, 202, 203, 204, 97, 206, 207, 208, 209, 210, 103, 212, 213, 214, 215, 216], [6, 12, 18, 24, 30, 37, 5, 11, 17, 23, 29, 38, 4, 10, 16, 22, 28, 39, 3, 9, 15, 21, 27, 40, 2, 8, 14, 20, 26, 41, 180, 174, 168, 162, 156, 42, 67, 61, 55, 49, 43, 73, 68, 62, 56, 50, 44, 182, 69, 63, 57, 51, 45, 183, 70, 64, 58, 52, 46, 184, 71, 65, 59, 53, 47, 185, 175, 176, 177, 178, 179, 181, 31, 25, 19, 13, 7, 1, 104, 98, 92, 86, 80, 74, 105, 99, 93, 87, 81, 75, 106, 100, 94, 88, 82, 76, 107, 101, 95, 89, 83, 77, 72, 66, 60, 54, 48, 186, 150, 110, 111, 112, 113, 114, 32, 116, 117, 118, 119, 120, 33, 122, 123, 124, 125, 126, 34, 128, 129, 130, 131, 132, 35, 134, 135, 136, 137, 138, 108, 102, 96, 90, 84, 78, 145, 146, 147, 148, 149, 211, 151, 152, 153, 154, 155, 205, 157, 158, 159, 160, 161, 199, 163, 164, 165, 166, 167, 193, 169, 170, 171, 172, 173, 187, 36, 140, 141, 142, 143, 144, 139, 133, 127, 121, 115, 109, 79, 188, 189, 190, 191, 192, 85, 194, 195, 196, 197, 198, 91, 200, 201, 202, 203, 204, 97, 206, 207, 208, 209, 210, 103, 212, 213, 214, 215, 216], [6, 143, 18, 24, 30, 37, 5, 173, 17, 23, 29, 38, 4, 167, 16, 22, 28, 39, 3, 161, 15, 21, 27, 40, 2, 155, 14, 20, 26, 41, 180, 149, 168, 162, 156, 42, 67, 61, 55, 49, 43, 73, 68, 62, 56, 50, 44, 182, 69, 63, 57, 51, 45, 183, 70, 64, 58, 52, 46, 184, 71, 65, 59, 53, 47, 185, 175, 176, 177, 178, 179, 181, 31, 12, 19, 13, 7, 1, 104, 11, 92, 86, 80, 74, 105, 10, 93, 87, 81, 75, 106, 9, 94, 88, 82, 76, 107, 8, 95, 89, 83, 77, 72, 174, 60, 54, 48, 186, 150, 110, 111, 112, 113, 114, 32, 116, 117, 118, 119, 120, 33, 122, 123, 124, 125, 126, 34, 128, 129, 130, 131, 132, 35, 134, 135, 136, 137, 138, 108, 102, 96, 90, 84, 78, 145, 146, 147, 148, 212, 211, 151, 152, 153, 154, 206, 205, 157, 158, 159, 160, 200, 199, 163, 164, 165, 166, 194, 193, 169, 170, 171, 172, 188, 187, 36, 140, 141, 142, 133, 144, 139, 25, 127, 121, 115, 109, 79, 98, 189, 190, 191, 192, 85, 99, 195, 196, 197, 198, 91, 100, 201, 202, 203, 204, 97, 101, 207, 208, 209, 210, 103, 66, 213, 214, 215, 216], [6, 143, 18, 24, 30, 37, 5, 173, 17, 23, 29, 38, 4, 167, 16, 22, 28, 39, 3, 161, 15, 21, 27, 40, 179, 47, 46, 45, 44, 43, 180, 149, 168, 162, 156, 42, 67, 61, 55, 49, 79, 73, 68, 62, 56, 50, 98, 182, 69, 63, 57, 51, 189, 183, 70, 64, 58, 52, 190, 184, 71, 65, 59, 53, 191, 185, 175, 176, 177, 178, 192, 181, 31, 12, 19, 13, 7, 1, 104, 11, 92, 86, 80, 74, 105, 10, 93, 87, 81, 75, 106, 9, 94, 88, 82, 76, 107, 8, 95, 89, 83, 77, 72, 174, 60, 54, 48, 186, 150, 2, 111, 112, 113, 114, 32, 155, 117, 118, 119, 120, 33, 14, 123, 124, 125, 126, 34, 20, 129, 130, 131, 132, 35, 26, 135, 136, 137, 138, 108, 41, 96, 90, 84, 78, 145, 146, 147, 148, 212, 211, 151, 152, 153, 154, 206, 205, 157, 158, 159, 160, 200, 199, 163, 164, 165, 166, 194, 193, 169, 170, 171, 172, 188, 187, 36, 140, 141, 142, 133, 144, 139, 25, 127, 121, 115, 109, 102, 134, 128, 122, 116, 110, 85, 99, 195, 196, 197, 198, 91, 100, 201, 202, 203, 204, 97, 101, 207, 208, 209, 210, 103, 66, 213, 214, 215, 216], [6, 143, 18, 24, 30, 37, 5, 173, 17, 23, 29, 38, 4, 167, 16, 22, 28, 39, 3, 161, 15, 21, 27, 40, 179, 47, 46, 45, 44, 43, 180, 149, 168, 162, 156, 42, 67, 61, 55, 49, 79, 73, 68, 62, 56, 50, 98, 182, 69, 63, 57, 51, 189, 183, 70, 64, 58, 52, 190, 184, 169, 170, 171, 172, 188, 187, 175, 176, 177, 178, 192, 181, 31, 12, 19, 13, 7, 1, 104, 11, 92, 86, 80, 74, 105, 10, 93, 87, 81, 75, 106, 9, 94, 88, 82, 76, 71, 65, 59, 53, 191, 185, 72, 174, 60, 54, 48, 186, 150, 2, 111, 112, 113, 114, 32, 155, 117, 118, 119, 120, 33, 14, 123, 124, 125, 126, 34, 20, 129, 130, 131, 132, 107, 8, 95, 89, 83, 77, 108, 41, 96, 90, 84, 78, 145, 146, 147, 148, 212, 211, 151, 152, 153, 154, 206, 205, 157, 158, 159, 160, 200, 199, 163, 164, 165, 166, 194, 193, 35, 26, 135, 136, 137, 138, 36, 140, 141, 142, 133, 144, 139, 25, 127, 121, 115, 109, 102, 134, 128, 122, 116, 110, 85, 99, 195, 196, 197, 198, 91, 100, 201, 202, 203, 204, 97, 101, 207, 208, 209, 210, 103, 66, 213, 214, 215, 216], [6, 143, 142, 24, 30, 37, 5, 173, 136, 23, 29, 38, 4, 167, 166, 22, 28, 39, 3, 161, 160, 21, 27, 40, 179, 47, 154, 45, 44, 43, 180, 149, 148, 162, 156, 42, 67, 61, 55, 49, 79, 73, 68, 62, 56, 50, 98, 182, 69, 63, 57, 51, 189, 183, 70, 64, 58, 52, 190, 184, 169, 170, 171, 172, 188, 187, 175, 176, 177, 178, 192, 181, 31, 12, 18, 13, 7, 1, 104, 11, 17, 86, 80, 74, 105, 10, 16, 87, 81, 75, 106, 9, 15, 88, 82, 76, 71, 65, 46, 53, 191, 185, 72, 174, 168, 54, 48, 186, 150, 2, 111, 112, 113, 114, 32, 155, 117, 118, 119, 120, 33, 14, 123, 124, 125, 126, 34, 20, 129, 130, 131, 132, 107, 8, 95, 89, 83, 77, 108, 41, 96, 90, 84, 78, 145, 146, 147, 213, 212, 211, 151, 152, 153, 207, 206, 205, 157, 158, 159, 201, 200, 199, 163, 164, 165, 195, 194, 193, 35, 26, 135, 128, 137, 138, 36, 140, 141, 127, 133, 144, 139, 25, 19, 121, 115, 109, 102, 134, 92, 122, 116, 110, 85, 99, 93, 196, 197, 198, 91, 100, 94, 202, 203, 204, 97, 101, 59, 208, 209, 210, 103, 66, 60, 214, 215, 216], [6, 143, 142, 24, 30, 37, 5, 173, 136, 23, 29, 38, 4, 167, 166, 22, 28, 39, 178, 172, 52, 51, 50, 49, 179, 47, 154, 45, 44, 43, 180, 149, 148, 162, 156, 42, 67, 61, 55, 85, 79, 73, 68, 62, 56, 99, 98, 182, 69, 63, 57, 93, 189, 183, 70, 64, 58, 196, 190, 184, 169, 170, 171, 197, 188, 187, 175, 176, 177, 198, 192, 181, 31, 12, 18, 13, 7, 1, 104, 11, 17, 86, 80, 74, 105, 10, 16, 87, 81, 75, 106, 9, 15, 88, 82, 76, 71, 65, 46, 53, 191, 185, 72, 174, 168, 54, 48, 186, 150, 2, 3, 112, 113, 114, 32, 155, 161, 118, 119, 120, 33, 14, 160, 124, 125, 126, 34, 20, 21, 130, 131, 132, 107, 8, 27, 89, 83, 77, 108, 41, 40, 90, 84, 78, 145, 146, 147, 213, 212, 211, 151, 152, 153, 207, 206, 205, 157, 158, 159, 201, 200, 199, 163, 164, 165, 195, 194, 193, 35, 26, 135, 128, 137, 138, 36, 140, 141, 127, 133, 144, 139, 25, 19, 121, 115, 109, 102, 134, 92, 122, 116, 110, 96, 95, 129, 123, 117, 111, 91, 100, 94, 202, 203, 204, 97, 101, 59, 208, 209, 210, 103, 66, 60, 214, 215, 216], [6, 143, 142, 24, 30, 37, 5, 173, 136, 23, 29, 38, 4, 167, 166, 22, 28, 39, 178, 172, 52, 51, 50, 49, 179, 47, 154, 45, 44, 43, 180, 149, 148, 162, 156, 42, 67, 61, 55, 85, 79, 73, 68, 62, 56, 99, 98, 182, 69, 63, 57, 93, 189, 183, 163, 164, 165, 195, 194, 193, 169, 170, 171, 197, 188, 187, 175, 176, 177, 198, 192, 181, 31, 12, 18, 13, 7, 1, 104, 11, 17, 86, 80, 74, 105, 10, 16, 87, 81, 75, 70, 64, 58, 196, 190, 184, 71, 65, 46, 53, 191, 185, 72, 174, 168, 54, 48, 186, 150, 2, 3, 112, 113, 114, 32, 155, 161, 118, 119, 120, 33, 14, 160, 124, 125, 126, 106, 9, 15, 88, 82, 76, 107, 8, 27, 89, 83, 77, 108, 41, 40, 90, 84, 78, 145, 146, 147, 213, 212, 211, 151, 152, 153, 207, 206, 205, 157, 158, 159, 201, 200, 199, 34, 20, 21, 130, 131, 132, 35, 26, 135, 128, 137, 138, 36, 140, 141, 127, 133, 144, 139, 25, 19, 121, 115, 109, 102, 134, 92, 122, 116, 110, 96, 95, 129, 123, 117, 111, 91, 100, 94, 202, 203, 204, 97, 101, 59, 208, 209, 210, 103, 66, 60, 214, 215, 216], [6, 143, 142, 141, 30, 37, 5, 173, 136, 135, 29, 38, 4, 167, 166, 21, 28, 39, 178, 172, 52, 159, 50, 49, 179, 47, 154, 153, 44, 43, 180, 149, 148, 147, 156, 42, 67, 61, 55, 85, 79, 73, 68, 62, 56, 99, 98, 182, 69, 63, 57, 93, 189, 183, 163, 164, 165, 195, 194, 193, 169, 170, 171, 197, 188, 187, 175, 176, 177, 198, 192, 181, 31, 12, 18, 24, 7, 1, 104, 11, 17, 23, 80, 74, 105, 10, 16, 22, 81, 75, 70, 64, 58, 51, 190, 184, 71, 65, 46, 45, 191, 185, 72, 174, 168, 162, 48, 186, 150, 2, 3, 112, 113, 114, 32, 155, 161, 118, 119, 120, 33, 14, 160, 124, 125, 126, 106, 9, 15, 88, 82, 76, 107, 8, 27, 89, 83, 77, 108, 41, 40, 90, 84, 78, 145, 146, 214, 213, 212, 211, 151, 152, 208, 207, 206, 205, 157, 158, 202, 201, 200, 199, 34, 20, 123, 130, 131, 132, 35, 26, 122, 128, 137, 138, 36, 140, 121, 127, 133, 144, 139, 25, 19, 13, 115, 109, 102, 134, 92, 86, 116, 110, 96, 95, 129, 87, 117, 111, 91, 100, 94, 196, 203, 204, 97, 101, 59, 53, 209, 210, 103, 66, 60, 54, 215, 216], [6, 143, 142, 141, 30, 37, 5, 173, 136, 135, 29, 38, 177, 171, 165, 57, 56, 55, 178, 172, 52, 159, 50, 49, 179, 47, 154, 153, 44, 43, 180, 149, 148, 147, 156, 42, 67, 61, 91, 85, 79, 73, 68, 62, 100, 99, 98, 182, 69, 63, 94, 93, 189, 183, 163, 164, 196, 195, 194, 193, 169, 170, 203, 197, 188, 187, 175, 176, 204, 198, 192, 181, 31, 12, 18, 24, 7, 1, 104, 11, 17, 23, 80, 74, 105, 10, 16, 22, 81, 75, 70, 64, 58, 51, 190, 184, 71, 65, 46, 45, 191, 185, 72, 174, 168, 162, 48, 186, 150, 2, 3, 4, 113, 114, 32, 155, 161, 167, 119, 120, 33, 14, 160, 166, 125, 126, 106, 9, 15, 21, 82, 76, 107, 8, 27, 28, 83, 77, 108, 41, 40, 39, 84, 78, 145, 146, 214, 213, 212, 211, 151, 152, 208, 207, 206, 205, 157, 158, 202, 201, 200, 199, 34, 20, 123, 130, 131, 132, 35, 26, 122, 128, 137, 138, 36, 140, 121, 127, 133, 144, 139, 25, 19, 13, 115, 109, 102, 134, 92, 86, 116, 110, 96, 95, 129, 87, 117, 111, 90, 89, 88, 124, 118, 112, 97, 101, 59, 53, 209, 210, 103, 66, 60, 54, 215, 216], [6, 143, 142, 141, 30, 37, 5, 173, 136, 135, 29, 38, 177, 171, 165, 57, 56, 55, 178, 172, 52, 159, 50, 49, 179, 47, 154, 153, 44, 43, 180, 149, 148, 147, 156, 42, 67, 61, 91, 85, 79, 73, 68, 62, 100, 99, 98, 182, 157, 158, 202, 201, 200, 199, 163, 164, 196, 195, 194, 193, 169, 170, 203, 197, 188, 187, 175, 176, 204, 198, 192, 181, 31, 12, 18, 24, 7, 1, 104, 11, 17, 23, 80, 74, 69, 63, 94, 93, 189, 183, 70, 64, 58, 51, 190, 184, 71, 65, 46, 45, 191, 185, 72, 174, 168, 162, 48, 186, 150, 2, 3, 4, 113, 114, 32, 155, 161, 167, 119, 120, 105, 10, 16, 22, 81, 75, 106, 9, 15, 21, 82, 76, 107, 8, 27, 28, 83, 77, 108, 41, 40, 39, 84, 78, 145, 146, 214, 213, 212, 211, 151, 152, 208, 207, 206, 205, 33, 14, 160, 166, 125, 126, 34, 20, 123, 130, 131, 132, 35, 26, 122, 128, 137, 138, 36, 140, 121, 127, 133, 144, 139, 25, 19, 13, 115, 109, 102, 134, 92, 86, 116, 110, 96, 95, 129, 87, 117, 111, 90, 89, 88, 124, 118, 112, 97, 101, 59, 53, 209, 210, 103, 66, 60, 54, 215, 216], [6, 143, 142, 141, 140, 37, 5, 173, 136, 135, 26, 38, 177, 171, 165, 57, 20, 55, 178, 172, 52, 159, 14, 49, 179, 47, 154, 153, 152, 43, 180, 149, 148, 147, 146, 42, 67, 61, 91, 85, 79, 73, 68, 62, 100, 99, 98, 182, 157, 158, 202, 201, 200, 199, 163, 164, 196, 195, 194, 193, 169, 170, 203, 197, 188, 187, 175, 176, 204, 198, 192, 181, 31, 12, 18, 24, 30, 1, 104, 11, 17, 23, 29, 74, 69, 63, 94, 93, 56, 183, 70, 64, 58, 51, 50, 184, 71, 65, 46, 45, 44, 185, 72, 174, 168, 162, 156, 186, 150, 2, 3, 4, 113, 114, 32, 155, 161, 167, 119, 120, 105, 10, 16, 22, 81, 75, 106, 9, 15, 21, 82, 76, 107, 8, 27, 28, 83, 77, 108, 41, 40, 39, 84, 78, 145, 215, 214, 213, 212, 211, 151, 209, 208, 207, 206, 205, 33, 118, 160, 166, 125, 126, 34, 117, 123, 130, 131, 132, 35, 116, 122, 128, 137, 138, 36, 115, 121, 127, 133, 144, 139, 25, 19, 13, 7, 109, 102, 134, 92, 86, 80, 110, 96, 95, 129, 87, 189, 111, 90, 89, 88, 124, 190, 112, 97, 101, 59, 53, 191, 210, 103, 66, 60, 54, 48, 216], [6, 143, 142, 141, 140, 37, 176, 170, 164, 158, 62, 61, 177, 171, 165, 57, 20, 55, 178, 172, 52, 159, 14, 49, 179, 47, 154, 153, 152, 43, 180, 149, 148, 147, 146, 42, 67, 97, 91, 85, 79, 73, 68, 101, 100, 99, 98, 182, 157, 59, 202, 201, 200, 199, 163, 53, 196, 195, 194, 193, 169, 191, 203, 197, 188, 187, 175, 210, 204, 198, 192, 181, 31, 12, 18, 24, 30, 1, 104, 11, 17, 23, 29, 74, 69, 63, 94, 93, 56, 183, 70, 64, 58, 51, 50, 184, 71, 65, 46, 45, 44, 185, 72, 174, 168, 162, 156, 186, 150, 2, 3, 4, 5, 114, 32, 155, 161, 167, 173, 120, 105, 10, 16, 22, 136, 75, 106, 9, 15, 21, 135, 76, 107, 8, 27, 28, 26, 77, 108, 41, 40, 39, 38, 78, 145, 215, 214, 213, 212, 211, 151, 209, 208, 207, 206, 205, 33, 118, 160, 166, 125, 126, 34, 117, 123, 130, 131, 132, 35, 116, 122, 128, 137, 138, 36, 115, 121, 127, 133, 144, 139, 25, 19, 13, 7, 109, 102, 134, 92, 86, 80, 110, 96, 95, 129, 87, 189, 111, 90, 89, 88, 124, 190, 112, 84, 83, 82, 81, 119, 113, 103, 66, 60, 54, 48, 216], [6, 143, 142, 141, 140, 37, 176, 170, 164, 158, 62, 61, 177, 171, 165, 57, 20, 55, 178, 172, 52, 159, 14, 49, 179, 47, 154, 153, 152, 43, 180, 149, 148, 147, 146, 42, 67, 97, 91, 85, 79, 73, 151, 209, 208, 207, 206, 205, 157, 59, 202, 201, 200, 199, 163, 53, 196, 195, 194, 193, 169, 191, 203, 197, 188, 187, 175, 210, 204, 198, 192, 181, 31, 12, 18, 24, 30, 1, 68, 101, 100, 99, 98, 182, 69, 63, 94, 93, 56, 183, 70, 64, 58, 51, 50, 184, 71, 65, 46, 45, 44, 185, 72, 174, 168, 162, 156, 186, 150, 2, 3, 4, 5, 114, 104, 11, 17, 23, 29, 74, 105, 10, 16, 22, 136, 75, 106, 9, 15, 21, 135, 76, 107, 8, 27, 28, 26, 77, 108, 41, 40, 39, 38, 78, 145, 215, 214, 213, 212, 211, 32, 155, 161, 167, 173, 120, 33, 118, 160, 166, 125, 126, 34, 117, 123, 130, 131, 132, 35, 116, 122, 128, 137, 138, 36, 115, 121, 127, 133, 144, 139, 25, 19, 13, 7, 109, 102, 134, 92, 86, 80, 110, 96, 95, 129, 87, 189, 111, 90, 89, 88, 124, 190, 112, 84, 83, 82, 81, 119, 113, 103, 66, 60, 54, 48, 216], [6, 143, 142, 141, 140, 36, 176, 170, 164, 158, 62, 35, 177, 171, 165, 57, 20, 34, 178, 172, 52, 159, 14, 33, 179, 47, 154, 153, 152, 32, 180, 149, 148, 147, 146, 145, 67, 97, 91, 85, 79, 73, 151, 209, 208, 207, 206, 205, 157, 59, 202, 201, 200, 199, 163, 53, 196, 195, 194, 193, 169, 191, 203, 197, 188, 187, 175, 210, 204, 198, 192, 181, 31, 12, 18, 24, 30, 37, 68, 101, 100, 99, 98, 61, 69, 63, 94, 93, 56, 55, 70, 64, 58, 51, 50, 49, 71, 65, 46, 45, 44, 43, 72, 174, 168, 162, 156, 42, 108, 107, 106, 105, 104, 150, 41, 8, 9, 10, 11, 2, 40, 27, 15, 16, 17, 3, 39, 28, 21, 22, 23, 4, 38, 26, 135, 136, 29, 5, 78, 77, 76, 75, 74, 114, 216, 215, 214, 213, 212, 211, 113, 155, 161, 167, 173, 120, 112, 118, 160, 166, 125, 126, 111, 117, 123, 130, 131, 132, 110, 116, 122, 128, 137, 138, 109, 115, 121, 127, 133, 144, 139, 25, 19, 13, 7, 1, 102, 134, 92, 86, 80, 182, 96, 95, 129, 87, 189, 183, 90, 89, 88, 124, 190, 184, 84, 83, 82, 81, 119, 185, 103, 66, 60, 54, 48, 186], [175, 169, 163, 157, 151, 67, 176, 170, 164, 158, 62, 35, 177, 171, 165, 57, 20, 34, 178, 172, 52, 159, 14, 33, 179, 47, 154, 153, 152, 32, 180, 149, 148, 147, 146, 145, 103, 97, 91, 85, 79, 73, 66, 209, 208, 207, 206, 205, 60, 59, 202, 201, 200, 199, 54, 53, 196, 195, 194, 193, 48, 191, 203, 197, 188, 187, 186, 210, 204, 198, 192, 181, 31, 12, 18, 24, 30, 37, 68, 101, 100, 99, 98, 61, 69, 63, 94, 93, 56, 55, 70, 64, 58, 51, 50, 49, 71, 65, 46, 45, 44, 43, 72, 174, 168, 162, 156, 42, 108, 107, 106, 105, 104, 6, 41, 8, 9, 10, 11, 143, 40, 27, 15, 16, 17, 142, 39, 28, 21, 22, 23, 141, 38, 26, 135, 136, 29, 140, 78, 77, 76, 75, 74, 36, 109, 110, 111, 112, 113, 216, 115, 116, 117, 118, 155, 215, 121, 122, 123, 160, 161, 214, 127, 128, 130, 166, 167, 213, 133, 137, 131, 125, 173, 212, 144, 138, 132, 126, 120, 211, 139, 25, 19, 13, 7, 1, 102, 134, 92, 86, 80, 182, 96, 95, 129, 87, 189, 183, 90, 89, 88, 124, 190, 184, 84, 83, 82, 81, 119, 185, 114, 5, 4, 3, 2, 150], [175, 169, 163, 157, 151, 67, 176, 170, 164, 158, 62, 35, 177, 171, 165, 57, 20, 34, 178, 172, 52, 159, 14, 33, 179, 47, 154, 153, 152, 32, 180, 149, 148, 147, 146, 145, 109, 110, 111, 112, 113, 216, 66, 209, 208, 207, 206, 205, 60, 59, 202, 201, 200, 199, 54, 53, 196, 195, 194, 193, 48, 191, 203, 197, 188, 187, 186, 210, 204, 198, 192, 181, 103, 97, 91, 85, 79, 73, 68, 101, 100, 99, 98, 61, 69, 63, 94, 93, 56, 55, 70, 64, 58, 51, 50, 49, 71, 65, 46, 45, 44, 43, 72, 174, 168, 162, 156, 42, 31, 12, 18, 24, 30, 37, 41, 8, 9, 10, 11, 143, 40, 27, 15, 16, 17, 142, 39, 28, 21, 22, 23, 141, 38, 26, 135, 136, 29, 140, 78, 77, 76, 75, 74, 36, 108, 107, 106, 105, 104, 6, 115, 116, 117, 118, 155, 215, 121, 122, 123, 160, 161, 214, 127, 128, 130, 166, 167, 213, 133, 137, 131, 125, 173, 212, 144, 138, 132, 126, 120, 211, 1, 182, 183, 184, 185, 150, 7, 80, 189, 190, 119, 2, 13, 86, 87, 124, 81, 3, 19, 92, 129, 88, 82, 4, 25, 134, 95, 89, 83, 5, 139, 102, 96, 90, 84, 114]]
        key_m_cube_2 = [i for i in range(1, 217, 1)]
        for i2 in step_array:
            key_m_cube_2 = self._mix_letter(text=key_m_cube_2, key=quick_rotate[i2], way=False)
        #key_m_cube_2 = self._cube_get_data_2(cube.cube.copy())
        #print("key_m_cube_2:\t", key_m_cube_2)

        text_scrambled = ""
        for i in text_formatted:
            text_scrambled += "".join(i2 for i2 in self._mix_letter(text=i, key=key_m_cube_2, way=encryption))# encryption -> eventuell Schlüssel umdrehen, da self._cube_int_to_moves(key_m_cube, 6, True)
        #text_scrambled = text # nur für tests da!
        
        if (len(text_scrambled) >= (20*20*6)) and not(encryption):
            cube_field_data_size_local = len(text_scrambled) // (20*20*6)
            key_m_cube_big = self.hilfsfunktionen.int2anybase(key_m_cube, 42)
            key_m_cube_big = int(str(self.get_key_m_cube(key_m_cube_big, 343, 1000)))
            text_scrambled = self.cube_big(text_scrambled, key_m_cube_big, 20, cube_field_data_size_local, encryption)

        return text_scrambled
    
    def cube_big(self, text, key_m_cube, cube_dimensions=0, cube_field_data_size=0, encryption=True) -> str:
        '''
        mappt <text> in <cube_field_data_size> großen stücken auf die oberfläche eines rubics-cube
        mit <cube_dimensions> "flächen" (das entscheidet also obs ein 3x3x3, 4x4x4, ... ist)

        dreht danach den würfel, abhängig von key_m_cube

        <encryption> = richtung der verschlüsselung: {True: verschlüsseln, False: entschlüsseln}

        -> return text_verdreht
        '''
        
        text = text[::-1]
        text_formatted = text[:(cube_dimensions**2 *6 *cube_field_data_size)]
        text = text[::-1]
        text_formatted = text_formatted[::-1]

        cube = self.cube_class(cube_dimensions, self.debug_c)
        cube.cube = self._cube_map_data(cube.cube.copy(), text_formatted, cube_field_data_size)
        #cube.print_cube()
        
        step_array = self._cube_int_to_moves(key_m_cube, cube_dimensions, encryption)
        #print("len(step_array): " + str(len(step_array)))
        for i in step_array:
            cube.rotate(i[0], i[1], i[2]+4)
        
        #cube.print_cube()
        #print()
        
        text_scrambled = text[:(len(text) - len(text_formatted))] + self._cube_get_data(cube.cube.copy())
        return text_scrambled


    class hilfsfunktionen():
        def __init__(self) -> None:
            pass

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





def run_test():
    global Y
    global N
    #print("new process")
    debug = False
    debug_c = False
    x = Verschlüsselung(debug=debug, debug_c=debug_c, debug_f=False)

    test = ""
    key = ""
    l1 = 1600#randint(10, 1600)
    l2 = 100#randint(20, 100)
    for i in range(l1*4): test += str(randint(0, 1))
    for i in range(l2): key += str(randint(0, 1))

    #if debug: print(test)
    encrypted = x.verschlüsseln(text=test, KEY=key)
    decrypted = x.entschlüsseln(encrypted, key)
    if test == decrypted:
        Y+=1
    else: N+=1; N_list.append((test, key))

def run_test_multiprocessing(data):
    r, von, bis, s = data[0], data[1], data[2], data[3]
    #print("new process")
    debug = False
    debug_c = False
    x = Verschlüsselung(debug=debug, debug_c=debug_c, debug_f=False)
    result = []
    
    #l1 = 1600#randint(10, 1600)
    l2 = 100#randint(20, 100)
    
    for i in range(von, bis+1, s):
        Y = 0
        N = 0
        t = time.time()
        for i2 in range(r):
            test = ""
            key = ""
            for i3 in range(i*8): test += str(randint(0, 1))
            for i3 in range(l2): key += str(randint(0, 1))
            
            #if debug: print(test)
            encrypted = x.verschlüsseln(text=test, KEY=key)
            decrypted = x.entschlüsseln(encrypted, key)
            if test == decrypted:
                Y+=1
            else: N+=1#; N_list.append((test, key))
        t = time.time() - t
        result.append([i, Y, N, t])
        #print("\nY:", Y, "|", "N:", N, "|", "D:", t)
    return result


if __name__ == "__main__":
    """q = []
    x = Verschlüsselung(debug=False)
    cube = x.cube_class(20)
    cube.cube = x._cube_map_data_2(cube.cube.copy(), [i for i in range(1, 2401, 1)], 1)
    for i in range(60):
        m = x._cube_int_to_moves(i,20,True)
        #print(m)
        cube_ = cube
        cube_.rotate(m[0][0], m[0][1], m[0][2])
        g = x._cube_get_data_2(cube_.cube)
        #print(m[0][0])
        q.append(g)
    #print(q)
    with open("quick_rotate_20", "w") as f:
        f.write(str(q))"""
    """Y = 0
    N = 0
    N_list = []
    p=[]
    t = time.time()
    r = 100
    print(f"0\tvon {r}", end="")
    for i in range(r):
        run_test()
        print(f"\r{i+1}\tvon {r}", end="")
    t = time.time() - t
    print("\nY:", Y, "|", "N:", N, "|", "D:", t)"""
    cores = 10
    anz = 100
    start = 1000
    stop = 1500
    step = 100
    work = [(anz, start, stop, step) for i in range(cores)]
    with multiprocessing.Pool(cores) as p: 
        data = p.map(run_test_multiprocessing, work)
    for i in range(len(data[0])):
        print(f"Text der länge {data[0][i][0]}\tY: {sum([i2[i][1] for i2 in data])} \t| N: {sum([i2[i][2] for i2 in data])} \t| D: {sum([i2[i][3] for i2 in data])} \t| {sum([i2[i][3] for i2 in data])/(cores*anz)}")
    
    #print(N_list)
    #x = Verschlüsselung(debug=True, debug_c=False, debug_f=True)
    #encrypted = x.verschlüsseln(text="0100100001100101011011000110110001101111001000000101011101101111011100100110110001100100", KEY="10000101010001010011011011010111111001101100101000111100")
    #print("".join(chr(i) for i in BitToInt(x.entschlüsseln(text=encrypted, KEY="10000101010001010011011011010111111001101100101000111100"))))
    

else:
    #print("erfolgreich Importiert: QED_system")
    pass
# just for fun
class fehler(ValueError): ...
