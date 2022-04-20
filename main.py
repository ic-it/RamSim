import argparse
import os


from crealization.callbacks import Callbacks
from crealization.ciostream import CIOstream
from crealization.cout import COut
from ramsim.executor import Executor
from ramsim.parser import Parser
from ramsim.register import Register


parser = argparse.ArgumentParser(description='Ram Sim by @ic-it')

parser.add_argument('source', type=str,
                    help='Source')

parser.add_argument('--split', '--spl', action='store_true',
                    help='Split')

parser.add_argument('--input', '-i', type=str,
                    help='Inputs file')

parser.add_argument('--output', '-o', type=str,
                    help='Outputs file')

parser.add_argument('--break-points', '--bp', nargs="+", type=int,
                    help='Break points')

args = parser.parse_args()

if args.input and os.path.exists(args.input):
    with open(args.input, 'r') as f:
        cios = CIOstream([int(i) for i in f.read().replace(" ", "").replace("\t", "").replace("\n", "").split(",")])
else:
    cios = CIOstream()

p = Parser(args.source, COut())

if p.parse():
    r = Register()
    e = Executor(p.parsed_data, COut(), cios, r, os.path.dirname(args.source) + "/", Callbacks(args.break_points, args.source))
    e.execute()

if args.output:
    with open(args.output, 'w') as f:
        f.write(", ".join([str(i) for i in cios.out]))