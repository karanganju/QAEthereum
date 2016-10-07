from ethereum import tester
from ethereum import utils
import serpent

from client import QClient
from client import AClient

state = tester.state()
contract = state.abi_contract(open('answers.se').read())

q1 = QClient(tester.k1, contract, state)
q2 = QClient(tester.k2, contract, state)
q3 = QClient(tester.k3, contract, state)
a4 = AClient(tester.k4, contract, state)
a5 = AClient(tester.k5, contract, state) 
a6 = AClient(tester.k6, contract, state)
a7 = AClient(tester.k7, contract, state)
a8 = AClient(tester.k8, contract, state)

# This is the simple generic case where everyone knows and plays by the rules and people act to vote the best answer which may
# or may not be aligned to their interests

q1.print_bal("q1:")
a4.print_bal("a4:")
a5.print_bal("a5:")
a6.print_bal("a6:")
a7.print_bal("a7:")
print "contract:", state.block.get_balance(contract.address)

q1.host("What ended in 1945?", 2000000000000)

# This period will now be the joining period. 

a4.join(q1, "THE NAZI DREAM!", 2000000000000)
a5.join(q1, "World War II", 2000000000000)

state.mine(1)

a6.join(q1, "World War I", 2000000000000)

state.mine(8)

a7.join(q1, "1944", 2000000000000)

state.mine(2)

a4.vote(q1, a5)

# The voting period starts after the previous vote

state.mine(2)

q1.vote(a5)
a7.vote(q1, a7)
state.mine(2)

a5.vote(q1, a5)
state.mine(2)

q1.print_bal("q1:")
a4.print_bal("a4:")
a5.print_bal("a5:")
a6.print_bal("a6:")
a7.print_bal("a7:")
print "contract:", state.block.get_balance(contract.address)

a7.reward(q1)

# Voting period now has ended

q1.print_bal("q1:")
a4.print_bal("a4:")
a5.print_bal("a5:")
a6.print_bal("a6:")
a7.print_bal("a7:")
print "contract:", state.block.get_balance(contract.address)