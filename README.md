# RamSim
## Random access machine emulator
[![Project Status: Inactive – The project has reached a stable, usable state but is no longer being actively developed; support/maintenance will be provided as time allows.](https://www.repostatus.org/badges/latest/inactive.svg)](https://www.repostatus.org/#inactive)

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
## Install
### Linux: 
```bash
chmod +x install.sh
./install.sh
```
If you are unable to install, write `python3 <dir to program>/main.py` instead of `ramsim`.

### Usage:
#### Help
    ramsim -h
#### Simple execute
    ramsim <file>
#### Select input file
    ramsim --input <file> <file>
#### Select output file
    ramsim --output <file> <file> 
#### Break points
    ramsim --break-points <list of int> --spl <file>
#### Example
    ramsim --input tests/1/args --output tests/1/out --bp 1 2 3 4 5 --spl tests/1/main.ram 

## Syntax Highlighting
You can add syntax highlighting to supported code editors
- [Sublime Text](./code-highlighting/sublime-text/README.md)