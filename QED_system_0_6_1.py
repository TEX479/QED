import math
from random import randint
import time
from multiprocessing import Pool



class Verschlüsselung():
    def __init__(self, chunk = 16, debug = True, cube_field_data_size = 1, debug_c=False, cores=1) -> None:
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
        self.cores = cores

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

        if key_mix>1: key_mix = int(key_mix%(len(text)//self.chunk))
        else: key_mix = int((key_mix*(len(text)//self.chunk))%(len(text)//self.chunk))

        key_start = int(S3[0]%(len(text)//self.chunk)) if S3[0]>=0 else int((S3[0]*(len(text)//self.chunk))%(len(text)//self.chunk))
        
        if self.debug: print("S3: ",S3)
        
        key_m_cube = self.get_key_m_cube(key_normal=key_normal, key_start=key_start)
        
        if len(key_normal)%2 == 0: key_normal = key_normal[:len(key_normal)-1]

        if self.debug: print("key_normal: ", key_normal, "\nstart: ", key_start, "\nmix: ", key_mix, "\nm_cube: ", key_m_cube, "\n")
        return {"n":key_normal, "s":key_start, "m":key_mix, "c":key_m_cube}

    def get_key_m_cube(self, key_normal:list, key_start:int) -> int:
        """
        erzeugt aus key_normal und key_start
        -> key_m_cube

        g? wird hier gesetzt
        """
        g=250
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
            key_m_cube = int("".join(str(i*10)[:-2] for i in key_m_cube))
            key_m_cube = self.hilfsfunktionen.int2anybase(number=key_m_cube, base=10)
        while len(key_m_cube) > g*1.7547956566698855:
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


        text = self.structure_mix_letter(way=True,full_text_=text, key=keys["m"])
        if self.debug: print("nach mix_letter: ", text, "\n")


        text_part = text[:keys["s"]*self.chunk]
        text_part = text_part[::-1]
        text_part = self.structure_m1(way=True, text=text_part, key=keys["n"].copy())
        text_part = text_part[::-1]
        text_ = text[keys["s"]*self.chunk:]
        text = text_part + text_#erw1
        if self.debug: print("nach erw1:       ", text, "\n")


        text = self.cube(text=text, key_m_cube=keys["c"], encryption=not(True), cores=self.cores)
        if self.debug: print("nach cube:       ", text, "\n")


        text = self.structure_m1(way=True, text=text, key=keys["n"].copy())
        if self.debug: print("nach m1:         ", text, "\n")

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


        text = self.structure_m1(way=False, text=text, key=keys["n"].copy())
        if self.debug: print("nach m1:         ", text, "\n")


        text = self.cube(text=text, key_m_cube=keys["c"], encryption=not(False), cores=self.cores)
        if self.debug: print("nach cube:       ", text, "\n")


        text_part = text[:keys["s"]*self.chunk]
        text_part = text_part[::-1]
        text_part = self.structure_m1(way=False, text=text_part, key=keys["n"].copy())
        text_part = text_part[::-1]
        text_ = text[keys["s"]*self.chunk:]
        text = text_part + text_#erw1
        if self.debug: print("nach erw1:       ", text, "\n")


        text = (self.structure_mix_letter(way=False, full_text_=text, key=keys["m"]))
        if self.debug: print("nach mix_letter: ", text, "\n")

        return text


    def VER_1(self, text:list, key:list, part:str, pos:int) -> str:
        """
        xor der Bits von part mit den von text nach key
        pos = position von part im text

        key umgedreht eingeben!
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
                    part = self.hilfsfunktionen.IntToBit((int(part, 2)^int(text[pos][:len(part)], 2)), len(part))
            else: 
                pos-=key[i]
                if pos < 0:
                    go_on = False

        return part

    def mix_letter(self,way,text:list,key:list) -> list:
        """
        mischt den text mit key
        way = richtung
        """
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
        erzeugt aus full_text_ und key einen schlüssel
        und teit den text
        ruft  mix_letter  auf
        way = richtung
        -> text vermischt
        """
        chunk = 4 #?
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
                try:
                    key_mix.index(full_text[key_])
                    go_on=False
                    last_number = full_text[key_]
                except:
                    key_mix.append(full_text[key_])

        key_mix_copy = key_mix.copy()
        if last_number != "": key_mix_copy.append(last_number)
        for i in range(len(key_mix)): key_mix[i] = int(key_mix[i],2) + 1
        s2 = key_mix.copy()
        s2.sort()
        for i in range(len(s2)):# alle Zahel aufeinanderfolgend 1.. bsp. 5 1 3 -> 3 1 2 
            key_mix[key_mix.index(s2[i])] = i+1
        for i in range(len(key_mix)):#keine Zahl doppelt?
            if key_mix.count(key_mix[i]) != 1:
                key_mix.pop(i)
        if self.debug: print("key_mix: ",key_mix)

        text_part1 = full_text[:key]
        if self.debug: print("Text_part_1 (1): ",text_part1)
        if not(text_end):
            text_part2 = full_text[key_+1:]
            if self.debug: print("Text_part_2 (1): ",text_part2)
               

        text_part1 = self.mix_letter(way=way,text=text_part1,key=key_mix)
        if self.debug: print("Text_part_1 (2): ",text_part1)
        full_text = text_part1
        full_text.extend(key_mix_copy)
        if not(text_end):
            text_part2 = self.mix_letter(way=way,text=text_part2,key=key_mix)
            if self.debug: print("Text_part_2 (2): ",text_part2)      
            full_text.extend(text_part2)
        if self.debug: print("text: ",full_text,"#")
        return "".join(i for i in full_text)

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

    def _parallel_cores(self, packed_data):
        """
        packed_data = ([("text_formatted1", cube_dimensions1), ...], step_array, nr, cube_field_data_size)
        erzeugt und dreht Würfel der größe cube_dimensions mit text_formatted auf den Flächen
        returnt (nr, text_scrambled) -> (int, ["", ...])
        """
        step_array = packed_data[1]
        nr = packed_data[2]
        cube_field_data_size = packed_data[3]

        text_scrambled = []
        for i in packed_data[0]:
            text_formatted = i[0]
            cube_dimensions = i[1]
            cube = self.cube_class(cube_dimensions, self.debug_c)
            cube.cube = self._cube_map_data(cube.cube.copy(), text_formatted, cube_field_data_size)
            for i in step_array:
                cube.rotate(i[0], i[1], i[2]+4)
            text_scrambled.append(self._cube_get_data(cube.cube.copy()))
        return (nr, text_scrambled)

    def cube(self, text, key_m_cube, cube_dimensions=0, cube_field_data_size=0, encryption=True, cores=0):
        '''
        mappt <text> in <cube_field_data_size> großen stücken auf die oberfläche eines rubics-cube
        mit <cube_dimensions> "flächen" (das entscheidet also obs ein 3x3x3, 4x4x4, ... ist)

        dreht danach den würfel, abhängig von key_m_cube

        <encryption> = richtung der verschlüsselung: {True: verschlüsseln, False: entschlüsseln}

        -> return text_verdreht
        '''
        if cube_field_data_size == 0:
            cube_field_data_size = self.cube_field_data_size

        if cube_dimensions == 0:
            cube_dimensions = int((len(text) // cube_field_data_size // 6) ** 0.5)
        
        if cube_dimensions == 0:
            raise fehler("\"text\" darf nicht kleiner (6 * \"cube_field_data_size\") sein.")
        
        text_formatted = []#[("text", cube_dimensions), ("text", cube_dimensions), ...]
        l = len(text)//cube_field_data_size
        while l >= 24:
            cube_dimensions = int((l//6)**0.5)
            if cube_dimensions > 6: cube_dimensions = 6
            text_formatted.append((text[:(cube_dimensions**2 *6)], cube_dimensions))
            text = text[(cube_dimensions**2 *6):]
            l = len(text)//cube_field_data_size

        #text_formatted = text[:(cube_dimensions**2 *6)]
        step_array = self._cube_int_to_moves(key_m_cube, cube_dimensions, encryption)
        work = []
        texts_per_core = math.ceil(len(text_formatted)/cores)
        for i in range(len(text_formatted)//texts_per_core):
            texts = text_formatted[i*texts_per_core : (i + 1)*texts_per_core]
            work.append((texts, step_array, i, cube_field_data_size))

        if len(text_formatted)//texts_per_core != len(text_formatted)/texts_per_core:
            h = len(text_formatted)%texts_per_core
            texts = text_formatted[-h:]
            work.append((texts,step_array, len(text_formatted)//texts_per_core, cube_field_data_size))

        if cores > 1:
            with Pool(len(work)) as p:
                text_scrambled = p.map(self._parallel_cores, work)
        else:
            text_scrambled = [self._parallel_cores(work[0])]
        if self.debug_c:print(text_scrambled)

        text_scrambled.sort()
        text_scrambled_ = ""
        for i in text_scrambled:
            text_scrambled_ += "".join(i2 for i2 in i[1])
        text_scrambled_ += text
        
        return text_scrambled_
    
    def cube_old(self, text, key_m_cube, cube_dimensions=0, cube_field_data_size=0, encryption=True):
        '''
        mappt <text> in <cube_field_data_size> großen stücken auf die oberfläche eines rubics-cube
        mit <cube_dimensions> "flächen" (das entscheidet also obs ein 3x3x3, 4x4x4, ... ist)

        dreht danach den würfel, abhängig von key_m_cube

        <encryption> = richtung der verschlüsselung: {True: verschlüsseln, False: entschlüsseln}

        -> return text_verdreht
        '''
        if cube_field_data_size == 0:
            cube_field_data_size = self.cube_field_data_size

        if cube_dimensions == 0:
            cube_dimensions = int((len(text) // cube_field_data_size // 6) ** 0.5)
        
        if cube_dimensions == 0:
            raise fehler("\"text\" darf nicht kleiner (6 * \"cube_field_data_size\") sein.")
        
        text_formatted = text[:(cube_dimensions**2 *6)]

        cube = self.cube_class(cube_dimensions, self.debug_c)
        cube.cube = self._cube_map_data(cube.cube.copy(), text_formatted, cube_field_data_size)
        #cube.print_cube()
        
        step_array = self._cube_int_to_moves(key_m_cube, cube_dimensions, encryption)
        #print("len(step_array): " + str(len(step_array)))

        for i in step_array:
            cube.rotate(i[0], i[1], i[2]+4)
        
        #cube.print_cube()
        #print()
        
        text_scrambled = self._cube_get_data(cube.cube.copy()) + text[len(text_formatted):]
        return text_scrambled


    class hilfsfunktionen():
        def __init__(self) -> None:
            pass

        def IntToBit(x:int, lenght = 8):
                return "0"*((math.ceil((len(bin(x))-2)/lenght)*lenght+2)-len(bin(x))) + bin(x)[2:]

        def int2anybase(number:int, base:int):
            number_ = []
            while number > 0:
                number_.append(number%base)
                number = number//base
            number_.reverse()
            return number_

        def int2anybase2(number:int, base:float):
            number_ = []
            l_komma = 10**len((str(base).split("."))[1])
            while number > 0:
                number_.append((number*l_komma)%(base*l_komma)/l_komma)
                number = (number*l_komma)//(base*l_komma)/l_komma
            number_.reverse()
            return number_

        def anybase2anybase(number_:list, input_base:int, output_base:int):
            number = 0
            for i in range(len(number_)):
                number += number_[len(number_)-i-1]*input_base**i

            output_number = []
            while number > 0:
                output_number.append(number%output_base)
                number = number//output_base

            output_number.reverse()
            return output_number





def run_test():
    global Y
    global N
    #print("new process")
    debug = False
    debug_c = False
    cores = 10
    x = Verschlüsselung(debug=debug, debug_c=debug_c, cores=cores)

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

if __name__ == "__main__":
    Y = 0
    N = 0
    N_list = []
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

else:
    #print("erfolgreich Importiert: QED_system")
    pass
# just for fun
class fehler(ValueError): ...
