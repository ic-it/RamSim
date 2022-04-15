from ramsim.executor import Executor
from ramsim.out import Out
from ramsim.parser import Parser
from ramsim.register import Register

p = Parser(open("test.ram", "r"), Out())

if p.parse():
    r = Register()
    e = Executor(p.parsed_data, Out(), r)
    e.execute()