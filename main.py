import argparse
import os
import sys


from crealization.callbacks import Callbacks
from crealization.ciostream import CIOstream
from crealization.cout import COut
from ramsim.executor import Executor
from ramsim.parser import Parser


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

p = Parser(os.path.abspath(args.source), COut())

if p.parse():
    e = Executor(p.parsed_data, COut(), cios, os.path.dirname(os.path.abspath(args.source)) + "/", Callbacks(args.break_points, os.path.abspath(args.source)))
    try:
        e.execute()
    except KeyboardInterrupt:
        print("\nStoped")
        sys.exit()

if args.output:
    with open(args.output, 'w') as f:
        f.write(", ".join([str(i) for i in cios.out]))