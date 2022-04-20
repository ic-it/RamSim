import argparse
import os
from ramsim.ciostream import CIOstream


from ramsim.executor import Executor
from ramsim.cout import COut
from ramsim.parser import Parser
from ramsim.register import Register


parser = argparse.ArgumentParser(description='Ram Sim by @ic-it')

parser.add_argument('source', type=str,
                    help='Source')

parser.add_argument('--step-by-step', action='store_true',
                    help='Step by step mode')

parser.add_argument('--input', type=str,
                    help='Inputs file')

parser.add_argument('--output', type=str,
                    help='Outputs file')

args = parser.parse_args()

if args.input:
    with open(args.input, 'r') as f:
        cios = CIOstream([int(i) for i in f.read().replace(" ", "").split(",")])
else:
    cios = CIOstream()

p = Parser(args.source, COut())

if p.parse():
    r = Register()
    e = Executor(p.parsed_data, COut(), cios, r, os.path.dirname(args.source) + "/")
    e.execute()

if args.output:
    with open(args.output, 'w') as f:
        f.write(", ".join([str(i) for i in cios.out]))