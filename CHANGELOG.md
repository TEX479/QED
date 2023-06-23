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

## [system_0_5_5_1](https://github.com/TEX479/QED/blob/main/QED_system_0_5_5_1.py) - 18.05.2023
### added
- `def Verschlüsselung.generate_key()` which takes length of the wanted key and returns a string containing the key

## [gui_0_4_2](https://github.com/TEX479/QED/blob/main/QED_GUI_0_4_2.py) - 18.05.2023
### added
- stuff to generate a random key and save it to a file
