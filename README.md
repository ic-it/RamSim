# RamSim
## Random access machine emulator
[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)

## Syntax:
```
links:
    1. explicit link (int)
    2. without link (=int)
    2. double link (*int)
MATH OPERATORS:
    1. ADD  +
    2. SUB  -
    3. MUL  *
    4. DIV  //
Label:
Syntax: "labelname:"

Comment:
Syntax: # asdasd
```
| Operator | Usage |
| ------ | ------ |
| LOAD | R[0] <- R[X] |
| STORE | R[0] -> R[X] |
| MATH OP | R[0] <- R[0] MATH OP R[X] |
| JMP or JUMP | Jump to label |
| JZ or JZERO | Jump to label if R[0] == 0 |
| JGZ or JGTZ | Jump to label if R[0] > 0 |
| HALT | Quit |
| INCLUDE | include file |
| PRINT | print string |

## About
I tried to make the program modular, so that if necessary, you can change the interfaces to it. In the `crealization` folder there are implementations of interfaces for `iostream` (input output data), `out` (output alerts) and `callbacks` (calls from within modules) through the console. The `main.py` file is an implementation for console. 

## Realization for console
### Usage:
#### Help
    python3 main.py -h
#### Simple execute
    python3 main.py <file>
#### Select input file
    python3 main.py --input <file> <file>
#### Select output file
    python3 main.py --output <file> <file> 
#### Break points
    python3 main.py --break-points <list of int> --spl <file>
#### Example
    python3 main.py --input tests/1/args --output tests/1/out --bp 1 2 3 4 5 --spl tests/1/main.ram 

## Syntax Highlighting
You can add syntax highlighting to supported code editors
- [Sublime Text](./code-highlighting/sublime-text/README.md)