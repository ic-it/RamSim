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
- [Sublime Text](./code-highlighting/sublime-text/README.md)