# Changelog
## [system_0_6_1](https://github.com/TEX479/QED/blob/main/QED_system_0_6_1.py) - 14.06.2023
### added
- `def cube_old()`: alte version der `cube()`-funktion

## [system_0_6_0](https://github.com/TEX479/QED/blob/main/QED_system_0_6_0.py) - 04.06.2023
### added
- `def generate_key(length)`: does exactly what you think it does. it generates a key of length `length`
- multiple comments for better readability
### fixed
- issue with running less than at least one core, crashing the programm

## [gui_0_4_3](https://github.com/TEX479/QED/blob/main/QED_GUI_0_4_3.py.py) - 26.05.2023
### removed
- `def BitToStr()`
### changed
- list to set cores -> button with str input
- adjustments for missing `BitToStr()`, replaced with `bytes()`
### added
- timing of de-/encryptionproccess

## [system_0_5_5_1](https://github.com/TEX479/QED/blob/main/QED_system_0_5_5_1.py) - 18.05.2023
### added
- funktion "Verschlüsselung.generate_key" which takes length of the wanted key and returns a string containing the key
### changed
- nothin
### fixed
- nothin

## [gui_0_4_2](https://github.com/TEX479/QED/blob/main/QED_GUI_0_4_2.py) - 18.05.2023
### added
- stuff to generate a random key and save it to a file
