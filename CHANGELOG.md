# Changelog
## [system_0_6_5](https://github.com/TEX479/QED/blob/main/QED_system_0_6_5.py) 22-23.06.2023
### changed
- minor changes for improvements/deletion of useless stuff

## [system_0_6_4](https://github.com/TEX479/QED/blob/main/QED_system_0_6_4.py) 15-20.06.2023
### fixed
- `cube_big()` wasn't working properly, now does

## [system_0_6_3](https://github.com/TEX479/QED/blob/main/QED_system_0_6_3.py) - 14.06.2023
### fixed
- `cube_big()` now has its own, longer (len() = 1000) `key_m_cube_big`
- ... and a bunch of other shit that broke
### changed
- `g` of `get_key_m_cube()` is now changable

## [system_0_6_2](https://github.com/TEX479/QED/blob/main/QED_system_0_6_2.py) - 14.06.2023
### fixed
- issue with `_parallel_cores()` where planes outside of `cube_dimensions` are turned
- generating `step_array` with 6 instead of `cube_dimensions` of last cube
### changed
- renamed & repurpoppsed `cube_old()` -> `cube_big()` with minor changes to workflow (back to front not front to back of text)
### added
- running `cube_big()` as a `20*20*20` cube taking as much of `cube()`'s `text` as possible to rotate

## [system_0_6_1](https://github.com/TEX479/QED/blob/main/QED_system_0_6_1.py) - 14.06.2023
### added
- `def cube_old()`: older version of `cube()` (used copypasta of "QED_system_0_5_0_1.py")

## [system_0_6_0](https://github.com/TEX479/QED/blob/main/QED_system_0_6_0.py) - 04.06.2023
### added
- `def generate_key(length)`: does exactly what you think it does. it generates a key of length `length`
- multiple comments for better readability
### fixed
- issue with running less than at least one core, crashing the programm

## [gui_0_4_3_special](https://github.com/TEX479/QED/blob/main/QED_GUI_0_4_3_special.py) - 04.06.2023
### added
- special feature, so you can input a text (can contain words :D), containing the number of cores to be used, which will be extracted as integer

## [gui_0_4_3](https://github.com/TEX479/QED/blob/main/QED_GUI_0_4_3.py) - 26.05.2023
### removed
- `def BitToStr()` (replaced by `bytes()`)
### changed
- list to set cores -> button with str input
- adjustments for missing `BitToStr()`, replaced with `bytes()`
### added
- timing of de-/encryption-proccess

## [system_0_5_5_2](https://github.com/TEX479/QED/blob/main/QED_system_0_5_5_2.py) - ???
### changed
- variable-names inside of `get_key()` for better readability
### added
- explanation-comment in `generate_key()`

## [system_0_5_5_1](https://github.com/TEX479/QED/blob/main/QED_system_0_5_5_1.py) - 18.05.2023
### added
- `def Verschlüsselung.generate_key()` which takes length of the wanted key and returns a string containing the key
### changed
- some comments again. added some, changed some, removed some.

## [gui_0_4_2](https://github.com/TEX479/QED/blob/main/QED_GUI_0_4_2.py) - 18.05.2023
### added
- stuff to generate a random key and save it to a file

## [system_0_5_5](https://github.com/TEX479/QED/QED_system_0_5_5.py) - ???
### added
- many comments stating the purpose of code for better readability
### changed
- something inside `structure_mix_letter()` to not include `StrToBit()` & `BitToStr()` anymore (bc the use of these functions was unnecessary)
### removed
- unneccesary comment (basically unused code) at the end of the file (this is dating back to the stoneage)
- `StrToBit()` & `BitToStr()` inside `hilfsfunktionen()`

## [system_0_5_4](https://github.com/TEX479/QED/QED_system_0_5_4.py) - ???
### changed
- `get_key()`: simplified `len(self.hilfsfunktionen.BitToStr(text, self.chunk))` to `len(text)//self.chunk`
### added
- any call of not cube related en- or decryption functions inside of `entschlüsseln()` & `verschlüsseln` that got removed in [system_0_5_1](https://github.com/TEX479/QED/blob/main/CHANGELOG.md#system_0_5_1---)

## [system_0_5_3](https://github.com/TEX479/QED/QED_system_0_5_3.py) - ???
### added
- `hilfsfunktionen.int2anybase2()` (i dont remember the difference)
- debug print of `step_array`s length inside of `_cube_int_to_moves()`
- some more algorithmic stuff for `get_key_m_cube()`

## [system_0_5_2](https://github.com/TEX479/QED/QED_system_0_5_2.py) - ???
### fixed
- issue inside of `cube()` where outputs of different cores where not handled correctly
### added
- algorithm for hashing-method inside of `get_key_m_cube()`, which is based on using different based numbers

## [system_0_5_1](https://github.com/TEX479/QED/QED_system_0_5_1.py) - ???
NOTE:
This version is the end of the `cube_class()`-branch. It combines both branches to the new 'main'-one. This means, there is now a `cube_class()` with implementation and all other changes of [system_0_4_3](https://github.com/TEX479/QED/blob/main/CHANGELOG.md#system_0_4_3---) and [system_0_4_2](https://github.com/TEX479/QED/blob/main/CHANGELOG.md#system_0_4_2---) are already implemented and might already be outdated. The merging happend within [system_0_5_0](https://github.com/TEX479/QED/blob/main/CHANGELOG.md#system_0_5_0-system_0_5_01--system_0_5_0_1---), [system_0_5_0(1)](https://github.com/TEX479/QED/blob/main/CHANGELOG.md#system_0_5_0-system_0_5_01--system_0_5_0_1---) & [system_0_5_0_1](https://github.com/TEX479/QED/blob/main/CHANGELOG.md#system_0_5_0-system_0_5_01--system_0_5_0_1---). There was much going on, so the merging process will just be skipped for this log. This means that this entry is a change comparision between [system_0_4_3](https://github.com/TEX479/QED/blob/main/CHANGELOG.md#system_0_4_3---) (and [system_0_4_2_k](https://github.com/TEX479/QED/blob/main/CHANGELOG.md#system_0_4_2_k---)) and [system_0_5_1](https://github.com/TEX479/QED/blob/main/CHANGELOG.md#system_0_5_1---)
### added
- `cube()`: function, called in `entschlüsseln()` & `verschlüsseln`. It mapps `text` to an `cube_dimensions`^3 rubics cube in chunks of `cube_field_data_size` and scrables/solves (depending on `encryption`) this cube using the `key_m_cube`
- `_cube_map_data()`: used to map information to the cubes faces
- `_cube_get_data()`: used to retrieve information from a given cubes faces
- `_cube_int_to_moves()`: used to generate the scramling moves for the cube. moves are generated based on `key_m_cube`
- `_parallel_cores()`: used to scramble/solve the cubes in parallel using pythons `multiprocessing` library.
- `hilfsfunktionen.anybase2anybase()`: capable of converting a list of integers to another list of integers, bith representing a number of some bases
### changed
- `StrToBit()`, `BitToStr()` and `IntToBit()` are now part of a class named `hilfsfunktionen()` inside of `Verschlüsselung()`
- `get_key()` (idk what the reason was, i might add it later on)
- complete change on `get_key_m_cube()`
- mostly reverted `VER_1()` to an older version that has better error handeling (if im not mistaking)
- inner workings of `structure_m1()` (probably as a bugfix, but who knows :man_shrugging:)
### removed
- any call of not cube related en- or decryption functions inside of `entschlüsseln()` & `verschlüsseln`

## [system_0_5_0](https://github.com/TEX479/QED/QED_system_0_5_0.py), [system_0_5_0(1)](https://github.com/TEX479/QED/QED_system_0_5_0(1).py) & [system_0_5_0_1](https://github.com/TEX479/QED/QED_system_0_5_0_1.py) - ???
NOTE:
Idk which version came first and they are kind of weird so i'll just ignore them for now. That also means, the changelog of `system_0_5_1` reffers to changes to `system_0_4_3`.

## [system_0_4_3](https://github.com/TEX479/QED/QED_system_0_4_3.py) - ???
This is still part of the 'main' branch, so a follow-up of `system_0_4_2`. There are some changes, working towards joining the  branches together
### added
- `get_key_m_cube()`: function to generate `key_m_cube` wich functions as a seed for rotating the rubics-cubes
### changed
- simplified and generalized `VER_1()` 
- simplified `structure_m1`

## [system_0_4_2_k](https://github.com/TEX479/QED/QED_system_0_4_2_k.py) - ???
### NOTE:
This version was created at the same time as `system_0_4_2`. there for it has not yet implemented its changes. So it's basically a fork of `system_0_4_1`.
### added
- `int2anybase()`: function that is capable of converting an integer to a list of integers, representing a number of any given base
- `cube_class()`: this class inside of `Verschlüsselung()` is a class, capable of simulating n-dimensional rubics-cubes (n: int, n > 0). This class is not beeing called yet.

## [system_0_4_2](https://github.com/TEX479/QED/QED_system_0_4_2.py) - ???
### changed
- `VER_1()` got a massive overhaul and now has a built in variable to work both ways (de- and encryption): `way: bool`
- `structure_m1()` now has better error handeling

## [system_0_4_1](https://github.com/TEX479/QED/QED_system_0_4_1.py) - ???
### fixed
- minor errors in `structure_mix_letter()` regarding `StrToBit()`
### removed
- just some debug print statements

## [system_0_4_0](https://github.com/TEX479/QED/QED_system_0_4_0.py) - ???
### fixed
- some minor stuff in `verschlüsseln()` & `entschlüsseln()`
### added
- some typehinting
### removed
- some commented code, wich isnt necesarry anymore
### changed
- `run_test()` now uses random inputs contrary to the previous fixed ones

## [system_0_4](https://github.com/TEX479/QED/QED_system_0_4.py) [dc-link](https://discord.com/channels/@me/641270189035487232/1080925878638358558) - ???
- same as 0_3, features didnt work fully, so they are mostly commented out, also had some errors, that where fixed
- [system_0_4_0](https://github.com/TEX479/QED/blob/main/CHANGELOG.md#system_0_4_0---) will contain a full update for the changelog since this will be the major new version

## [system_0_3_](https://github.com/TEX479/QED/QED_system_0_3_.py) - ???
### fixed
- idk, probably some minor fixes as well
### added
- textformatting in `verschlüsseln()` & `entschlüsseln()`
- fixed inputs for `run_test()`

## [system_0_3](https://github.com/TEX479/QED/QED_system_0_3.py) - ???
- just a version previous to 0_3_, features didnt work fully, so they are mostly commented out
- `system_0_3_` will contain a full update for the changelog since this will be the major new version

## [system_0_2](https://github.com/TEX479/QED/QED_system_0_2.py) - ???
### fixed
- minor fixes in `get_key()`
- something not working in `structure_mix_letter()`
### changed
- almost entire `mix_letter()`
- `run_test()` and other testing-purposed code
- `structure_mix_letter()` uses a local `chunk` variable
### removed
- some `if self.debug: print()` statements
- not working bits in `entschlüsseln()` & `verschlüsseln()`
- comment to improve `VER_1()`
- comment to speed up `structure_m1()`

## [system_0_1](https://github.com/TEX479/QED/QED_system_0_1.py) - ???
idk what even happend here. many things got changed, added or removed
### fixed
- multiple bugs, for example
### changed
- `text['o']`, `text['v']` & `tex['e']` -> `text: str`
### added
- `run_test()`: does exactly what you think it does
- multiple print statements for debugging purposes (after each conversion of text)
- type-hinting for output of functions

## [gui_0](https://github.com/TEX479/QED/QED_GUI_0.py) - ???
- started using the system/gui seperation bc it's just better

## [system_0](https://github.com/TEX479/QED/QED_system_0.py) - ???
- started using the system/gui seperation bc it's just better
