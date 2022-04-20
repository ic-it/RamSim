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


## Usage:
#### Help
    python3 cui.py -h
#### Simple execute
    python3 cui.py <file>
#### Select input file
    python3 cui.py --input <file> <file>
#### Select output file
    python3 cui.py --output <file> <file> 
#### Example
    python3 cui.py --input tests/args --output tests/out tests/test.ram 

