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


# This attack scenario shows how late voters can be biased by voting early. The only solution to this problem is to somehow
# make the votes of each person private but that has not been tackled at this stage and so the protocol does not defend against
# this attack.

# However, this attack also showcases how the protocol is safe from some trivial attacks such as calling vote or reward functions
# before the deadline to gain an undue advantage. Also, it shows how we incentivize people to vote by keeping their ether in escrow
# and providing them the chance to obtain a small chunk of it.

# Also, this escrow system makes sure that the system moves forward. Since, at least one of the participants woul have a chance
# of winning, there would be at least one participant who would have incentive to call the reward function. Mostly, in the open
# vote system given in the code, we can assume that this will generally be the person with the most votes or rarely his voters.

###################   ATTACK CASE I  #########################
############  THE CASE OF THE QUICK VOTER  ###################

q1.print_bal("q1:")
a4.print_bal("a4:")
a5.print_bal("a5:")
a6.print_bal("a6:")
a7.print_bal("a7:")
a8.print_bal("a8:")
print "contract:", state.block.get_balance(contract.address)

q1.host("What ended in 1945?", 2000000000000)

# This period will now be the joining period. 

a4.join(q1, "THE NAZI DREAM!", 2000000000000)
a5.join(q1, "World War II", 2000000000000)
state.mine(1)

# This step will return 0 because of the min_bid condition

print a6.join(q1, "World War I", 1000000)
state.mine(2)

# So will the next two as the joining phase is still going on (for a total of 11 blocks as hard-coded in answers.se)

print a5.vote(q1, a5)
print a5.reward(q1)
state.mine(6)

a7.join(q1, "1944", 2000000000000)
state.mine(2)

# At this point the joining phase is still ongoing, but will stop as soon as the first call to vote is made.
# It seems intuitive that a confident respondent will take this call

a4.vote(q1, a4)

# The join will now fail

print a8.join(q1, "Deutschland!!!", 4000000000000)
state.mine(2)

q1.vote(a7)
a7.vote(q1, a7)
state.mine(2)

# So will the reward, which a7 could have potentially called earlier to get the reward now

print a7.reward(q1)

# One thing to note here is that for a5, there is no incentive to vote for himself as he will not get any rewards
# Secondly, there is no incentive for a5 to vote for a7 either, because if he votes for a4, it will be a tie and due
# to the simplistic manner of choosing ties that we have taken (first answer), a4 will win and a5 will have the voters
# cut all to himself, whereas in the other case, he would have to share it with q1
# Thirdly, even if our manner of choosing ties was randomized, his expected reward on voting for a4 would still be more
# Hence, if a7 is rational, he will choose to vote for a4

# Another thing to note is that if a7s money was not escrowed, he would have stopped contributing by now and so the protocol
# incentivizes players by keeping their initial bids

a5.vote(q1, a4)
state.mine(2)

q1.print_bal("q1:")
a4.print_bal("a4:")
a5.print_bal("a5:")
a6.print_bal("a6:")
a7.print_bal("a7:")
a8.print_bal("a8:")
print "contract:", state.block.get_balance(contract.address)

# Again, at this point the voting phase is still running (although there aren't any voters left) and will stop as the
# first call to reward is made. It seems intuitive here that a4 would want to take the call again.

a4.reward(q1)

# It is critical to notice how any person in place of a4 could manipulate his chances of winning by just voting 
# himself first very early on

q1.print_bal("q1:")
a4.print_bal("a4:")
a5.print_bal("a5:")
a6.print_bal("a6:")
a7.print_bal("a7:")
a8.print_bal("a8:")
print "contract:", state.block.get_balance(contract.address)