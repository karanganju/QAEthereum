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
a4_dual = AClient(tester.k5, contract, state) 
a6 = AClient(tester.k6, contract, state)
a7 = AClient(tester.k7, contract, state)
a8 = AClient(tester.k8, contract, state)


# This attack scenario shows how richer voters can bias results by having multiple votes. Again, the bias itself can be nullified
# by revealing votes after the reward phase but if the voter gains majority just by placing that many bids as different
# respondents which vote to a single respondent, then we cannot prevent it. However, lets see how much an attacker benefits by 
# 'buying respondents' (which is what we'll call the issue above). 

# We assume the the attacker has only 1 respondent with minimum bid x where the other repondents contribute a total of y. 
# Taking the voters cut to be a fraction c and the number of voters in favour to be t, if the attacker gets the reward, 
# it will be (x+y)*(1-c) + (x+y)*c/t and his profit will be his reward - x = y*(1-c + c/t) + x*(c/t - c). Clearly, his profit
# is inversely proportional to x. Although t might increase if he 'buys respondents', it will increase by 1 while x will at
# least double. Hence, the attacker would want to buy the least number of respondents to win the votes.

# Whether that would pose a problem would require a deeper game theoretic analysis.

###################   ATTACK CASE II  #########################
##########  THE CASE OF THE INFLUENTIAL VOTER  ################

q1.print_bal("q1:")
a4.print_bal("a4:")
a4_dual.print_bal("a4_dual:")
a6.print_bal("a6:")
a7.print_bal("a7:")
a8.print_bal("a8:")
print "contract:", state.block.get_balance(contract.address)

q1.host("What is the science of classifying things?", 2000000000000)

# This period will now be the joining period. 

a4.join(q1, "Classification", 2000000000000)
a4_dual.join(q1, "Taxi", 2000000000000)
state.mine(3)

# Another thing one can note here is that there really is no incentive for a player to bid any amount higher than the minimum
# bit amount. The more a player bids, the more has to be given out either to the winner or to the voters. But what could be 
# beneficial to a player could be to split his funds and bid using 2 instances as a4 is doing. Doing that gives you 2 votes 
# and consequently much more voting power but at an extra cost

a6.join(q1, "Taxonomy", 2000000000000)
a7.join(q1, "IDK", 2000000000000)
a8.join(q1, "IDK", 2000000000000)

state.mine(9)

a6.vote(q1, a6)
a4.vote(q1, a4)
a4_dual.vote(q1, a4)

state.mine(4)

# Now, assuming that a7 mines before a8, he has 4 choices ->
# a4_dual/a7/a8 but that can only win if a8 also agrees with him and given the tie breaking condition we have employed,
# he has no chance of winning the voters cut with any of those choices
# a6 but he can only make it a tie which will eventually lose unless a8 also agrees with hem
# That leaves the safest choice to be a4 which is clearly a poor choice

a7.vote(q1, a4)
a7.vote(q1, a4)

state.mine(3)

q1.print_bal("q1:")
a4.print_bal("a4:")
a4_dual.print_bal("a4_dual:")
a6.print_bal("a6:")
a7.print_bal("a7:")
a8.print_bal("a8:")
print "contract:", state.block.get_balance(contract.address)

print a4.reward(q1)

q1.print_bal("q1:")
a4.print_bal("a4:")
a4_dual.print_bal("a4_dual:")
a6.print_bal("a6:")
a7.print_bal("a7:")
a8.print_bal("a8:")
print "contract:", state.block.get_balance(contract.address)